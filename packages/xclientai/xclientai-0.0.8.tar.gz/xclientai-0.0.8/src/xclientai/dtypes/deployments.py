from typing import List, Any, Dict, Optional
from pydantic import BaseModel, Field, validator
import re
from enum import Enum
from xclientai.dtypes.shared import Status, Credentials, MachineType, Metadata
    
   
class ModelSpecs(BaseModel):
    model_path: Optional[str]
    credentials: Optional[Credentials]

class Batcher(BaseModel):
    max_batch_size: Optional[int] = 1
    # Max latency in milliseconds
    max_lantecy: Optional[int] = 1
    # batch request timeout in milliseconds
    # 20 secs by default
    timeout: Optional[int] = 20000

class SCALE_METRIC(str, Enum):
    CONCURRENCY = "concurrency"
    RPS = "rps"

class Scaling(BaseModel):
    time_before_scaling_to_zero: Optional[int] = 1800000
    min_replicas: Optional[int] = 1
    max_replicas: Optional[int] = 1
    scale_metric: Optional[SCALE_METRIC] = SCALE_METRIC.CONCURRENCY
    target_scaling_value: Optional[int] = 1
    
    @validator("min_replicas")
    def validate_min_replicas(cls, v):
        assert v >= 0, "min_replicas value of the scaling config cannot be lower than 0"
            
        return v
    
    @validator("max_replicas")
    def validate_max_replicas(cls, v, values):
        assert v >= 0, "max_replicas value of the scaling config cannot be lower than 0"
        
        assert v >= values['min_replicas'], "max_replicas value of the scaling config cannot be lower than the min_replicas value"
            
        return v
    
    @validator("scale_metric")
    def validate_scale_metric(cls, v):
        valid_scale_metrics = [SCALE_METRIC.CONCURRENCY, SCALE_METRIC.RPS]
        
        assert v in valid_scale_metrics, "The allowed scale_metrics are SCALE_METRIC.CONCURRENCY, SCALE_METRIC.RPS"
        
        return v
    
    @validator("target_scaling_value")
    def validate_target_scaling_value(cls, v):
        assert v >= 0, "target_scaling_value value of the scaling config cannot be lower than 0"

        return v
    
    class Config:
        validate_all = True 

    
class DeploymentSpecs(BaseModel):
    batcher: Optional[Batcher] = Field(default_factory=Batcher)
    scaling: Optional[Scaling] = Field(default_factory=Scaling)
    
    
class Inference(BaseModel):
    base_endpoint: Optional[str]
    is_ready_endpoint: Optional[str]
    infer_endpoint: Optional[str]
    api_key: Optional[str]
    
    
class DeploymentContainerSpecs(BaseModel):
    machine_type: MachineType = MachineType.GPU_T4_1
    spot: Optional[bool] = True
    image: Optional[str]
    command: Optional[List[str]]
    args: Optional[List[str]]
    env: Optional[Dict[str, str]]
    secrets: Optional[Dict[str, str]] = Field(repr=False)
    

class Deployment(BaseModel):
    deployment_name: str
    status: Status = Status.NOT_STARTED
    model_specs: ModelSpecs
    deployment_specs: Optional[DeploymentSpecs] = Field(default_factory=DeploymentSpecs)
    container_specs: DeploymentContainerSpecs
    inference: Optional[Inference]
    metadata: Optional[Metadata]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_all = True 
        
    @validator("deployment_name")
    def validate_deployment_name(cls, v):
        regex = "^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$"
        
        assert len(v) <= 30, "The deployment name cannot be longuer than 30 characters. Currently {}".format(len(v))
        
        assert bool(re.match(regex, v)), "The deployment_name must consist of lower case alphanumeric characters. Regex used for validation is '^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$'"
        
        return v   
