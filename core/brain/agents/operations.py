from dataclasses import dataclass
import subprocess
import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)

@dataclass
class SRE_Sentinel:
    """
    The Reliability Engineer Agent.
    Responsible for monitoring system health, docker containers, and logs.
    """
    
    def check_docker_health(self) -> Dict[str, str]:
        """Checks the status of running docker containers."""
        try:
            # Run docker ps to get status
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}:{{.Status}}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            health_map = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        health_map[parts[0]] = parts[1]
            
            return health_map
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker check failed: {e}")
            return {"error": "Docker CLI failed or not installed"}
        except FileNotFoundError:
             return {"error": "Docker executable not found"}

    def analyze_logs(self, service_name: str, lines: int = 50) -> List[str]:
        """Fetches and scans logs for errors."""
        try:
            result = subprocess.run(
                ["docker", "logs", "--tail", str(lines), service_name],
                capture_output=True,
                text=True
            )
            
            logs = result.stdout + result.stderr
            error_lines = []
            
            for line in logs.split('\n'):
                if "ERROR" in line or "CRITICAL" in line or "Exception" in line:
                    error_lines.append(line)
            
            return error_lines
        except Exception as e:
            logger.error(f"Log analysis failed for {service_name}: {e}")
            return [f"Could not fetch logs: {str(e)}"]

    def system_status_report(self) -> Dict[str, Any]:
        """Generates a full system health report."""
        containers = self.check_docker_health()
        
        # Check critical services
        critical_services = ["azuracast", "icecast", "liquidsoap"] # Hypothetical names
        issues = []
        
        for svc in critical_services:
            # Loose matching for container names
            found = False
            for name, status in containers.items():
                if svc in name:
                    found = True
                    if "Up" not in status:
                        issues.append(f"Service {name} is not Up ({status})")
                    break
            # Note: Not flagging "not found" strictly here as names vary
            
        status = "HEALTHY" if not issues else "DEGRADED"
        
        return {
            "status": status,
            "issues": issues,
            "containers": containers
        }
