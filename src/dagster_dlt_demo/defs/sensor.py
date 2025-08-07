import json
import dagster as dg
from dagster_dlt_demo.sftp.sftp_service import SFTPClient
from datetime import datetime, timedelta
import pytz
from dagster_dlt_demo.defs.jobs import dummy_job

sftp_client_instance = SFTPClient(
    hostName=dg.EnvVar("hostName").get_value(),
    port=dg.EnvVar("port").get_value(),
    userName=dg.EnvVar("userName").get_value(),
    password=dg.EnvVar("password").get_value(),
)


def sftp_sensor(name: str, job_def, filename_pattern: str = "", remote_path: str = "."):
    @dg.sensor(name=name, job=job_def, default_status=dg.DefaultSensorStatus.RUNNING)
    def sftp_sensor(context: dg.SensorEvaluationContext):
        try:
            conn = sftp_client_instance.connect()

            cursor_data = json.loads(context.cursor) if context.cursor else {}
            last_st_mtime = cursor_data.get("last_st_mtime", 0)

            result = sftp_client_instance.get_latest(
                conn, remote_path, filename_pattern, last_st_mtime
            )

            if result and result.get("file") and result["file_mtime"] > last_st_mtime:
                file_mtime = result["file_mtime"]
                file_obj = result["file"]
                dir_name = result["dir_name"]

                new_cursor = {
                    "last_st_mtime": file_mtime,
                    "last_dir_name": dir_name,
                    "last_filename": file_obj.filename,
                }
                context.update_cursor(json.dumps(new_cursor))

                sydney_tz = pytz.timezone("Australia/Sydney")
                now_sydney = datetime.now(sydney_tz) - timedelta(1)
                date_str = now_sydney.strftime("%Y-%m-%d")
                return dg.RunRequest(
                    run_key=f"daily_upload_{date_str}"
                )
            else:
                return dg.SkipReason(
                    f"No new files matching '{filename_pattern}' found"
                )

        except Exception as e:
            context.log.error(f"SFTP check failed: {e}")
            return dg.SkipReason(f"SFTP connection failed: {e}")
        finally:
            try:
                context.log.info("Sensor success!!!")
                sftp_client_instance.close()
            except:
                pass

    return sftp_sensor


sensors = [
    sftp_sensor(
        name="sftp_sensor",
        job_def=dummy_job,
        filename_pattern="orders.csv",
        remote_path="input/",
    )
]
