from xclientai.utils.requests_utils import do_request
from xclientai.config import Config
from xclientai.dtypes.executor import ExecutionJob
from typing import List, Optional


class ExecutionJobsClient:
    
    @classmethod
    def get_jobs(cls, workspace_id: Optional[str] = None) -> List[ExecutionJob]:        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.EXECUTION_BASE_URL_X_BACKEND
            ),
            http_method="get",
            workspace_id=workspace_id
        )
        
        list_job_dicts = response.json()["data"]
        jobs = []
        
        for job_dict in list_job_dicts:
            job = ExecutionJob.parse_obj(job_dict)
            jobs.append(job)
            
        return jobs
    
    @classmethod
    def get_job_by_name(cls, job_name: str, workspace_id: Optional[str] = None) -> ExecutionJob:        
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get",
            workspace_id=workspace_id
        )
        
        job_dict = response.json()["data"]
        job = ExecutionJob.parse_obj(job_dict)
        
        return job
    
    @classmethod
    def get_logs(cls, job_name: str, workspace_id: Optional[str] = None) -> List[ExecutionJob]:        
        response = do_request(
            url="{}/v1/jobs/{}/logs".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get",
            workspace_id=workspace_id
        )
        
        logs = response.json()["data"]
        
        return logs
    
    @classmethod
    def cancel_job(cls, job_name: str, reason: str = "", workspace_id: Optional[str] = None) -> ExecutionJob:
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            params={
                "hard_delete": False,
                "reason": reason
            },
            http_method="delete",
            workspace_id=workspace_id
        )
        
        job_dict = response.json()["data"]
        job = ExecutionJob.parse_obj(job_dict)
        return job
    
    @classmethod
    def delete_job(cls, job_name: str, reason: str = "", workspace_id: Optional[str] = None) -> ExecutionJob:
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.EXECUTION_BASE_URL_X_BACKEND,
                job_name
            ),
            params={
                "hard_delete": True,
                "reason": reason
            },
            http_method="delete",
            workspace_id=workspace_id
        )
        
        job_dict = response.json()["data"]
        job = ExecutionJob.parse_obj(job_dict)
        return job
    
    @classmethod
    def create_job(cls, job: ExecutionJob, reason: str = "", workspace_id: Optional[str] = None) -> ExecutionJob:        
        job_dict = job.dict()
        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.EXECUTION_BASE_URL_X_BACKEND
            ),
            params={
                "reason": reason
            },
            http_method="post",
            json_data=job_dict,
            workspace_id=workspace_id
        )
        
        returned_job_dict = response.json()["data"]
        returned_job = ExecutionJob.parse_obj(returned_job_dict)
        
        return returned_job
       