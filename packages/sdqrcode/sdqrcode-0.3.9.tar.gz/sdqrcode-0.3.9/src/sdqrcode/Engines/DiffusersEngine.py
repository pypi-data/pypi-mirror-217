import sdqrcode.Engines.Engine as Engine

from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    StableDiffusionControlNetImg2ImgPipeline,
    UniPCMultistepScheduler,
)
import torch
import transformers
from diffusers import UniPCMultistepScheduler
from diffusers import DPMSolverMultistepScheduler
import PIL
import torch

# [diffusers.schedulers.scheduling_ddim.DDIMScheduler,
#  diffusers.schedulers.scheduling_euler_ancestral_discrete.EulerAncestralDiscreteScheduler,
#  diffusers.schedulers.scheduling_lms_discrete.LMSDiscreteScheduler,
#  diffusers.schedulers.scheduling_dpmsolver_singlestep.DPMSolverSinglestepScheduler,
#  diffusers.schedulers.scheduling_k_dpm_2_discrete.KDPM2DiscreteScheduler,
#  diffusers.schedulers.scheduling_heun_discrete.HeunDiscreteScheduler,
#  diffusers.schedulers.scheduling_deis_multistep.DEISMultistepScheduler,
#  diffusers.schedulers.scheduling_euler_discrete.EulerDiscreteScheduler,
#  diffusers.schedulers.scheduling_k_dpm_2_ancestral_discrete.KDPM2AncestralDiscreteScheduler,
#  diffusers.schedulers.scheduling_unipc_multistep.UniPCMultistepScheduler,
#  diffusers.schedulers.scheduling_ddpm.DDPMScheduler,
#  diffusers.utils.dummy_torch_and_torchsde_objects.DPMSolverSDEScheduler,
#  diffusers.schedulers.scheduling_dpmsolver_multistep.DPMSolverMultistepScheduler,
#  diffusers.schedulers.scheduling_pndm.PNDMScheduler]

from diffusers.schedulers.scheduling_ddim import DDIMScheduler
from diffusers.schedulers.scheduling_euler_ancestral_discrete import (
    EulerAncestralDiscreteScheduler,
)
from diffusers.schedulers.scheduling_lms_discrete import LMSDiscreteScheduler
from diffusers.schedulers.scheduling_dpmsolver_singlestep import (
    DPMSolverSinglestepScheduler,
)
from diffusers.schedulers.scheduling_k_dpm_2_discrete import KDPM2DiscreteScheduler
from diffusers.schedulers.scheduling_heun_discrete import HeunDiscreteScheduler
from diffusers.schedulers.scheduling_deis_multistep import DEISMultistepScheduler
from diffusers.schedulers.scheduling_euler_discrete import EulerDiscreteScheduler
from diffusers.schedulers.scheduling_k_dpm_2_ancestral_discrete import (
    KDPM2AncestralDiscreteScheduler,
)
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
from diffusers.schedulers.scheduling_ddpm import DDPMScheduler
from diffusers.utils.dummy_torch_and_torchsde_objects import DPMSolverSDEScheduler
from diffusers.schedulers.scheduling_dpmsolver_multistep import (
    DPMSolverMultistepScheduler,
)
from diffusers.schedulers.scheduling_pndm import PNDMScheduler


class DiffusersEngine(Engine.Engine):
    def __init__(self, config, torch_dtype):
        super().__init__(config)

        self.controlnet_units = []
        for name, unit in self.config["controlnet_units"].items():
            cn_unit = ControlNetModel.from_pretrained(unit["model"], torch_dtype=torch_dtype)
            self.controlnet_units.append(cn_unit)
        
        
        
        if len(self.controlnet_units) == 1:
            self.controlnet_units = self.controlnet_units[0]
            
        if self.config["global"]["mode"] == "txt2img":  
            self.pipeline = StableDiffusionControlNetPipeline.from_pretrained(
                self.config["global"]["model_name_or_path"],
                controlnet=self.controlnet_units,
                torch_dtype=torch_dtype,
            )
        
        if self.config["global"]["mode"] == "img2img":
            self.pipeline = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
                self.config["global"]["model_name_or_path"],
                controlnet=self.controlnet_units,
                torch_dtype=torch_dtype,
            )
        self.pipeline.enable_xformers_memory_efficient_attention()
        self.pipeline = self.pipeline.to("cuda")


    def generate_sd_qrcode(
        self,
        input_image: PIL.Image.Image = None,
        controlnet_input_images: PIL.Image.Image = None,
    ) -> list[PIL.Image.Image]:
        controlnet_weights = [
            unit["weight"] for unit in self.config["controlnet_units"].values()
        ]
        
        guidance_starts = [
            unit["start"] for unit in self.config["controlnet_units"].values()
        ]
        
        guidance_stops = [
            unit["end"] for unit in self.config["controlnet_units"].values()
        ]

        self.pipeline.scheduler = get_scheduler(
            self.config["global"]["scheduler_name"],
            self.pipeline.scheduler.config,
        )
        
        seeded_generator = torch.Generator(device="cuda").manual_seed(
            self.config["global"]["seed"]
        ) if self.config["global"]["seed"] != -1 else None

        
        # fix bug when only one image is provided in the list
        if len(controlnet_input_images) == 1:
            controlnet_input_images = controlnet_input_images[0]
        if len(controlnet_weights) == 1:
            controlnet_weights = controlnet_weights[0]
        if len(guidance_starts) == 1:
            guidance_starts = guidance_starts[0]
        if len(guidance_stops) == 1:
            guidance_stops = guidance_stops[0]
            
        if self.config["global"]["mode"] == "txt2img":
            r = self.pipeline(
                generator=seeded_generator,
                prompt=self.config["global"]["prompt"],
                negative_prompt=self.config["global"]["negative_prompt"],
                width=self.config["global"]["width"],
                height=self.config["global"]["height"],
                num_inference_steps=self.config["global"]["steps"],
                image=controlnet_input_images,
                controlnet_conditioning_scale=controlnet_weights,
                num_images_per_prompt=self.config["global"]["batch_size"],
                control_guidance_start=guidance_starts,
                control_guidance_end=guidance_stops,
            )
        
        if self.config["global"]["mode"] == "img2img":
            r = self.pipeline(
                prompt=self.config["global"]["prompt"],
                image=input_image,
                negative_prompt=self.config["global"]["negative_prompt"],
                width=self.config["global"]["width"],
                height=self.config["global"]["height"],
                num_inference_steps=self.config["global"]["steps"],
                control_image=controlnet_input_images,
                controlnet_conditioning_scale=controlnet_weights,
                generator=seeded_generator,
                control_guidance_start=guidance_starts,
                control_guidance_end=guidance_stops,

                num_images_per_prompt=self.config["global"]["batch_size"],
            )

        return r.images




def get_scheduler(scheduler_name: str, config_scheduler):
    if scheduler_name == "DDIM":
        return DDIMScheduler.from_config(config_scheduler)
    if scheduler_name == "Euler":
        return EulerDiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "Euler a":
        return EulerAncestralDiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "LMS":
        return LMSDiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM2 Karras":
        return KDPM2DiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM2 a Karras":
        return KDPM2AncestralDiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "Heun":
        return HeunDiscreteScheduler.from_config(config_scheduler)
    if scheduler_name == "DDPM":
        return DDPMScheduler.from_config(config_scheduler)
    if scheduler_name == "UniPC":
        return UniPCMultistepScheduler.from_config(config_scheduler)
    if scheduler_name == "PNDM":
        return PNDMScheduler.from_config(config_scheduler)
    if scheduler_name == "DEI":
        return DEISMultistepScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM++ SDE":
        return DPMSolverSDEScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM++ 2S a":
        return DPMSolverSinglestepScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM++ 2M":
        return DPMSolverMultistepScheduler.from_config(config_scheduler)
    if scheduler_name == "DPM++ SDE Karras":
        return DPMSolverSDEScheduler.from_config(
            config_scheduler, use_karras_sigmas=True
        )
    if scheduler_name == "DPM++ 2S a Karras":
        return DPMSolverSinglestepScheduler.from_config(
            config_scheduler, use_karras_sigmas=True
        )
    if scheduler_name == "DPM++ 2M Karras":
        return DPMSolverMultistepScheduler.from_config(
            config_scheduler, use_karras_sigmas=True
        )

    raise ValueError(f"Scheduler {scheduler_name} not found")
