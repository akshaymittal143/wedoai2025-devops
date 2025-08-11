#!/usr/bin/env python3
"""
AI-Powered Anomaly Detection for DevOps Pipeline
Simulates ML-based anomaly detection with explainable AI reporting
"""

import json
import random
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MetricData:
    """Represents a metric data point"""
    timestamp: datetime
    service: str
    metric_name: str
    value: float
    labels: Dict[str, str]

@dataclass
class AnomalyResult:
    """Represents an anomaly detection result"""
    detected: bool
    confidence: float
    severity: str
    metric: str
    service: str
    explanation: str
    recommended_actions: List[str]
    impact_estimate: str

class AIAnomalyDetector:
    """
    Simulated AI-powered anomaly detection system
    In production, this would use real ML models like Isolation Forest,
    LSTM networks, or transformer models for time series anomaly detection
    """
    
    def __init__(self):
        self.baseline_metrics = {
            "error_rate": 0.02,  # 2% baseline error rate
            "response_time": 0.5,  # 500ms baseline response time
            "cpu_usage": 0.3,  # 30% baseline CPU usage
            "memory_usage": 0.4,  # 40% baseline memory usage
            "request_rate": 100,  # 100 req/sec baseline
        }
        
    def detect_anomalies(self, metrics: List[MetricData]) -> List[AnomalyResult]:
        """
        Detect anomalies in the provided metrics
        This simulates AI-based anomaly detection
        """
        anomalies = []
        
        for metric in metrics:
            anomaly = self._analyze_metric(metric)
            if anomaly.detected:
                anomalies.append(anomaly)
                
        return anomalies
    
    def _analyze_metric(self, metric: MetricData) -> AnomalyResult:
        """Analyze a single metric for anomalies"""
        baseline = self.baseline_metrics.get(metric.metric_name, 0)
        
        # Simulate ML model prediction
        if metric.metric_name == "error_rate":
            return self._analyze_error_rate(metric, baseline)
        elif metric.metric_name == "response_time":
            return self._analyze_response_time(metric, baseline)
        elif metric.metric_name == "cpu_usage":
            return self._analyze_cpu_usage(metric, baseline)
        else:
            return AnomalyResult(
                detected=False,
                confidence=0.0,
                severity="none",
                metric=metric.metric_name,
                service=metric.service,
                explanation="No anomaly detected",
                recommended_actions=[],
                impact_estimate="None"
            )
    
    def _analyze_error_rate(self, metric: MetricData, baseline: float) -> AnomalyResult:
        """Analyze error rate for anomalies"""
        threshold = baseline * 3  # 3x baseline is anomalous
        
        if metric.value > threshold:
            confidence = min(0.95, (metric.value - baseline) / baseline)
            severity = "critical" if metric.value > baseline * 5 else "high"
            
            return AnomalyResult(
                detected=True,
                confidence=confidence,
                severity=severity,
                metric=metric.metric_name,
                service=metric.service,
                explanation=f"Error rate {metric.value:.3f} is {metric.value/baseline:.1f}x higher than baseline ({baseline:.3f}). This indicates potential issues with service reliability.",
                recommended_actions=[
                    "Investigate recent deployments or configuration changes",
                    "Check application logs for specific error patterns",
                    "Verify external dependencies are functioning properly",
                    "Consider rolling back to previous version if issues persist"
                ],
                impact_estimate=f"${int(metric.value * 1000)}/hour in lost revenue" if severity == "critical" else "Medium business impact"
            )
        
        return AnomalyResult(detected=False, confidence=0.0, severity="none", metric=metric.metric_name, service=metric.service, explanation="Normal error rate", recommended_actions=[], impact_estimate="None")
    
    def _analyze_response_time(self, metric: MetricData, baseline: float) -> AnomalyResult:
        """Analyze response time for anomalies"""
        threshold = baseline * 2  # 2x baseline response time is concerning
        
        if metric.value > threshold:
            confidence = min(0.9, (metric.value - baseline) / baseline)
            severity = "high" if metric.value > baseline * 4 else "medium"
            
            return AnomalyResult(
                detected=True,
                confidence=confidence,
                severity=severity,
                metric=metric.metric_name,
                service=metric.service,
                explanation=f"Response time {metric.value:.3f}s is {metric.value/baseline:.1f}x higher than baseline ({baseline:.3f}s). Users may experience slow application performance.",
                recommended_actions=[
                    "Scale up application pods to handle increased load",
                    "Check database query performance and connection pools",
                    "Analyze CPU and memory usage patterns",
                    "Review recent code changes for performance regressions"
                ],
                impact_estimate="20% user satisfaction decrease" if severity == "high" else "Minor user experience impact"
            )
        
        return AnomalyResult(detected=False, confidence=0.0, severity="none", metric=metric.metric_name, service=metric.service, explanation="Normal response time", recommended_actions=[], impact_estimate="None")
    
    def _analyze_cpu_usage(self, metric: MetricData, baseline: float) -> AnomalyResult:
        """Analyze CPU usage for anomalies"""
        if metric.value > 0.8:  # 80% CPU usage is concerning
            confidence = min(0.85, (metric.value - baseline) / baseline)
            severity = "critical" if metric.value > 0.9 else "high"
            
            return AnomalyResult(
                detected=True,
                confidence=confidence,
                severity=severity,
                metric=metric.metric_name,
                service=metric.service,
                explanation=f"CPU usage {metric.value:.1%} is critically high (baseline: {baseline:.1%}). This may indicate resource exhaustion or potential security issues like crypto-mining.",
                recommended_actions=[
                    "Immediately check for unusual processes or security breaches",
                    "Scale horizontal pod autoscaler limits if legitimate load",
                    "Investigate potential memory leaks or infinite loops",
                    "Review resource requests and limits configuration"
                ],
                impact_estimate="Service degradation imminent" if severity == "critical" else "Performance degradation likely"
            )
        
        return AnomalyResult(detected=False, confidence=0.0, severity="none", metric=metric.metric_name, service=metric.service, explanation="Normal CPU usage", recommended_actions=[], impact_estimate="None")

class ExplainableAIReporter:
    """Generate human-readable incident reports with AI explanations"""
    
    def generate_incident_report(self, anomalies: List[AnomalyResult]) -> str:
        """Generate a comprehensive incident report"""
        if not anomalies:
            return "✅ No anomalies detected. All systems operating normally."
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_anomalies = sorted(anomalies, key=lambda x: severity_order.get(x.severity, 4))
        
        report = []
        report.append("🚨 ANOMALY DETECTION REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        report.append(f"Total Anomalies: {len(anomalies)}")
        report.append("")
        
        for i, anomaly in enumerate(sorted_anomalies, 1):
            report.append(f"## Anomaly #{i}: {anomaly.severity.upper()}")
            report.append(f"**Service:** {anomaly.service}")
            report.append(f"**Metric:** {anomaly.metric}")
            report.append(f"**Confidence:** {anomaly.confidence:.1%}")
            report.append(f"**Impact:** {anomaly.impact_estimate}")
            report.append("")
            report.append(f"**🤖 AI Analysis:**")
            report.append(anomaly.explanation)
            report.append("")
            report.append("**📋 Recommended Actions:**")
            for action in anomaly.recommended_actions:
                report.append(f"- {action}")
            report.append("")
            report.append("-" * 40)
            report.append("")
        
        # Add correlation analysis
        if len(anomalies) > 1:
            report.append("## 🔗 Correlation Analysis")
            report.append("Multiple anomalies detected simultaneously.")
            report.append("This pattern suggests a systemic issue that may require coordinated response.")
            report.append("")
        
        return "\n".join(report)

def simulate_metrics() -> List[MetricData]:
    """Generate simulated metrics data"""
    services = ["ai-devops-demo", "product-details", "payments-service", "user-profiles"]
    metrics = []
    
    base_time = datetime.utcnow()
    
    for i in range(20):  # Generate 20 data points
        timestamp = base_time - timedelta(minutes=i*5)
        service = random.choice(services)
        
        # Simulate some anomalies
        if random.random() < 0.2:  # 20% chance of anomaly
            if random.random() < 0.5:
                # Error rate spike
                metrics.append(MetricData(
                    timestamp=timestamp,
                    service=service,
                    metric_name="error_rate",
                    value=random.uniform(0.1, 0.3),  # High error rate
                    labels={"endpoint": "/api/upload"}
                ))
            else:
                # CPU spike
                metrics.append(MetricData(
                    timestamp=timestamp,
                    service=service,
                    metric_name="cpu_usage",
                    value=random.uniform(0.85, 0.95),  # High CPU
                    labels={"pod": f"{service}-{random.randint(1,3)}"}
                ))
        else:
            # Normal metrics
            metrics.append(MetricData(
                timestamp=timestamp,
                service=service,
                metric_name="error_rate",
                value=random.uniform(0.01, 0.04),  # Normal error rate
                labels={"endpoint": "/api/health"}
            ))
    
    return metrics

def main():
    """Main execution function for demonstration"""
    logger.info("🤖 AI-Powered Anomaly Detection System Starting...")
    
    # Initialize the AI detector
    detector = AIAnomalyDetector()
    reporter = ExplainableAIReporter()
    
    # Simulate getting metrics (in production, this would come from Prometheus/monitoring)
    logger.info("📊 Analyzing metrics data...")
    metrics = simulate_metrics()
    
    # Detect anomalies
    anomalies = detector.detect_anomalies(metrics)
    
    # Generate and display report
    report = reporter.generate_incident_report(anomalies)
    print(report)
    
    # Save report to file
    report_file = f"anomaly_report_{int(time.time())}.txt"
    with open(report_file, 'w') as f:
        f.write(report)
    
    logger.info(f"📄 Report saved to: {report_file}")
    
    if anomalies:
        logger.warning(f"⚠️  {len(anomalies)} anomalies detected!")
        return 1
    else:
        logger.info("✅ No anomalies detected - all systems normal")
        return 0

if __name__ == "__main__":
    exit(main())
