export enum AirflowDagRunStateEnum {
    Queued = "queued",
    Running = "running",
    Success = "success",
    Failed = "failed",
}

export interface AirflowDagRunResponse {
    conf: any;
    dag_id: string;
    dag_run_id: string;
    end_date: string;
    execution_date: string;
    external_trigger: boolean;
    logical_date: string;
    start_date: string;
    state: AirflowDagRunStateEnum;
}

export interface AirflowTask {
    dagID: string;
    dagRunID: string;
    state: AirflowDagRunStateEnum;
    successMessage?: string;
    failedMessage?: string;
}
