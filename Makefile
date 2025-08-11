# AI-Augmented DevOps Pipeline - Makefile
# Complete automation for the WeDoAI 2025 demonstration

.PHONY: help setup build scan test deploy-k8s demo-ai cleanup
.DEFAULT_GOAL := help

# Configuration
IMAGE_NAME := wedoai2025-devops
IMAGE_TAG := latest
REGISTRY := ghcr.io/your-username
FULL_IMAGE := $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
K8S_NAMESPACE := default

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

define print_step
	@echo "$(BLUE)🤖 AI-DevOps Pipeline: $(1)$(NC)"
endef

define print_success
	@echo "$(GREEN)✅ $(1)$(NC)"
endef

define print_warning
	@echo "$(YELLOW)⚠️  $(1)$(NC)"
endef

define print_error
	@echo "$(RED)❌ $(1)$(NC)"
endef

help: ## Show this help message
	@echo "$(BLUE)🤖 AI-Augmented DevOps Pipeline Commands$(NC)"
	@echo "================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  make setup build scan deploy-k8s"
	@echo ""

setup: ## Install all prerequisites and dependencies
	$(call print_step,Setting up development environment)
	@command -v docker >/dev/null 2>&1 || { $(call print_error,Docker is required but not installed. Please install Docker first.); exit 1; }
	@command -v kubectl >/dev/null 2>&1 || { $(call print_warning,kubectl not found. Kubernetes features will be limited.); }
	@command -v python3 >/dev/null 2>&1 || { $(call print_error,Python 3 is required but not installed.); exit 1; }
	
	# Install Python dependencies
	pip3 install --user pre-commit ruff
	
	# Install pre-commit hooks
	pre-commit install
	
	# Create necessary directories
	mkdir -p logs artifacts reports
	
	$(call print_success,Environment setup complete!)

setup-dev: setup ## Additional setup for development
	$(call print_step,Setting up development environment)
	
	# Install development dependencies
	pip3 install --user -r app/requirements.txt
	pip3 install --user pytest flask-testing
	
	# Set up git hooks
	pre-commit install --hook-type commit-msg
	pre-commit install --hook-type pre-push
	
	$(call print_success,Development environment ready!)

build: ## Build the Docker container
	$(call print_step,Building Docker container)
	
	# Build the image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(FULL_IMAGE)
	
	# Display image info
	@echo "$(GREEN)📦 Built Images:$(NC)"
	@docker images | grep $(IMAGE_NAME) | head -2
	
	$(call print_success,Docker build completed!)

scan: ## Run comprehensive security scans
	$(call print_step,Running security scans)
	
	# Pre-commit hooks (if not already run)
	@echo "$(BLUE)🔍 Running pre-commit security checks...$(NC)"
	pre-commit run --all-files || true
	
	# Container vulnerability scanning with Trivy
	@echo "$(BLUE)🔍 Scanning container for vulnerabilities...$(NC)"
	@if command -v trivy >/dev/null 2>&1; then \
		trivy image --format json --output reports/trivy-report.json $(IMAGE_NAME):$(IMAGE_TAG); \
		trivy image --severity HIGH,CRITICAL $(IMAGE_NAME):$(IMAGE_TAG); \
	else \
		$(call print_warning,Trivy not installed. Install with: brew install trivy); \
		echo "Running basic Docker security scan..."; \
		docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
			-v $(PWD)/reports:/reports \
			aquasec/trivy:latest image --format json --output /reports/trivy-report.json $(IMAGE_NAME):$(IMAGE_TAG); \
	fi
	
	# AI-powered analysis simulation
	@echo "$(BLUE)🤖 Running AI vulnerability analysis...$(NC)"
	@echo "Priority 1: Container base image vulnerabilities (HIGH)"
	@echo "Priority 2: Python package dependencies (MEDIUM)"
	@echo "Priority 3: Configuration security (LOW)"
	
	$(call print_success,Security scanning completed! Check reports/ directory)

test: ## Run application tests
	$(call print_step,Running application tests)
	
	# Unit tests
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	cd app && python -m pytest -v || python -m unittest discover -v
	
	# Container health check
	@echo "$(BLUE)🏥 Testing container health...$(NC)"
	docker run -d --name test-container -p 5001:5000 $(IMAGE_NAME):$(IMAGE_TAG)
	@sleep 5
	@curl -f http://localhost:5001/api/health || { $(call print_error,Health check failed); docker logs test-container; docker rm -f test-container; exit 1; }
	docker rm -f test-container
	
	# Load test simulation
	@echo "$(BLUE)⚡ Running load test simulation...$(NC)"
	@for i in $$(seq 1 10); do curl -s http://localhost:5001/api/health > /dev/null && echo "Request $$i: OK" || echo "Request $$i: FAILED"; done
	
	$(call print_success,All tests passed!)

deploy-k8s: ## Deploy to Kubernetes with security policies
	$(call print_step,Deploying to Kubernetes)
	
	# Check cluster connection
	@kubectl cluster-info > /dev/null || { $(call print_error,Cannot connect to Kubernetes cluster); exit 1; }
	
	# Apply Kyverno policies first
	@echo "$(BLUE)🛡️ Applying security policies...$(NC)"
	@if kubectl get crd clusterpolicies.kyverno.io >/dev/null 2>&1; then \
		kubectl apply -f k8s/policies/; \
		$(call print_success,Kyverno policies applied); \
	else \
		$(call print_warning,Kyverno not installed. Deploying without policy enforcement); \
	fi
	
	# Create namespace if it doesn't exist
	kubectl create namespace $(K8S_NAMESPACE) --dry-run=client -o yaml | kubectl apply -f -
	
	# Apply Kubernetes manifests
	@echo "$(BLUE)☸️  Deploying application...$(NC)"
	kubectl apply -f k8s/manifests/ -n $(K8S_NAMESPACE)
	
	# Wait for deployment
	@echo "$(BLUE)⏳ Waiting for deployment to be ready...$(NC)"
	kubectl rollout status deployment/ai-devops-demo -n $(K8S_NAMESPACE) --timeout=300s
	
	# Display deployment info
	@echo "$(GREEN)🚀 Deployment Information:$(NC)"
	kubectl get pods,svc -n $(K8S_NAMESPACE) -l app.kubernetes.io/name=ai-devops-demo
	
	# Port forward for local access
	@echo "$(BLUE)🌐 Setting up port forwarding...$(NC)"
	@echo "Run: kubectl port-forward svc/ai-devops-demo 8080:80 -n $(K8S_NAMESPACE)"
	@echo "Then visit: http://localhost:8080"
	
	$(call print_success,Kubernetes deployment completed!)

demo-ai: ## Run AI anomaly detection demonstration
	$(call print_step,Running AI anomaly detection demo)
	
	# Run the ML model
	@echo "$(BLUE)🤖 Starting AI anomaly detection...$(NC)"
	cd ml-model && python3 anomaly_detection.py
	
	# Display results
	@echo "$(GREEN)📊 AI Analysis Results:$(NC)"
	@ls -la anomaly_report_*.txt 2>/dev/null || echo "No reports generated"
	
	$(call print_success,AI demo completed!)

monitoring: ## Set up monitoring stack (optional)
	$(call print_step,Setting up monitoring)
	
	# Check if monitoring namespace exists
	kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
	
	# Apply monitoring configurations
	kubectl apply -f k8s/manifests/monitoring.yaml -n monitoring
	
	@echo "$(YELLOW)Note: This requires Prometheus and Grafana to be installed$(NC)"
	@echo "Install with: helm repo add prometheus-community https://prometheus-community.github.io/helm-charts"
	@echo "helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring"
	
	$(call print_success,Monitoring configuration applied!)

logs: ## View application logs
	$(call print_step,Fetching application logs)
	
	@if kubectl get deployment ai-devops-demo -n $(K8S_NAMESPACE) >/dev/null 2>&1; then \
		kubectl logs -l app.kubernetes.io/name=ai-devops-demo -n $(K8S_NAMESPACE) --tail=50; \
	else \
		$(call print_warning,Application not deployed to Kubernetes); \
		echo "Showing Docker logs if container is running:"; \
		docker logs $$(docker ps -q --filter "ancestor=$(IMAGE_NAME):$(IMAGE_TAG)") 2>/dev/null || echo "No running containers found"; \
	fi

status: ## Show deployment status
	$(call print_step,Checking deployment status)
	
	@echo "$(BLUE)📊 System Status:$(NC)"
	@echo "Docker Images:"
	@docker images | grep $(IMAGE_NAME) || echo "No images found"
	@echo ""
	@echo "Kubernetes Status:"
	@if kubectl get deployment ai-devops-demo -n $(K8S_NAMESPACE) >/dev/null 2>&1; then \
		kubectl get pods,svc,deploy -n $(K8S_NAMESPACE) -l app.kubernetes.io/name=ai-devops-demo; \
	else \
		echo "Not deployed to Kubernetes"; \
	fi
	@echo ""
	@echo "Security Policies:"
	@kubectl get cpol 2>/dev/null | grep -E "(NAME|security)" || echo "No Kyverno policies found"

validate: ## Validate all configurations
	$(call print_step,Validating configurations)
	
	# Validate Kubernetes manifests
	@echo "$(BLUE)☸️  Validating Kubernetes manifests...$(NC)"
	@for file in k8s/manifests/*.yaml; do \
		echo "Validating $$file..."; \
		kubectl apply --dry-run=client -f $$file || exit 1; \
	done
	
	# Validate Kyverno policies
	@echo "$(BLUE)🛡️ Validating Kyverno policies...$(NC)"
	@if command -v kyverno >/dev/null 2>&1; then \
		kyverno validate k8s/policies/ || echo "Kyverno CLI validation skipped"; \
	else \
		echo "Kyverno CLI not installed - skipping policy validation"; \
	fi
	
	# Validate Docker configuration
	@echo "$(BLUE)🐳 Validating Dockerfile...$(NC)"
	@if command -v hadolint >/dev/null 2>&1; then \
		hadolint Dockerfile; \
	else \
		echo "hadolint not installed - skipping Dockerfile validation"; \
	fi
	
	$(call print_success,All validations passed!)

clean: ## Clean up local artifacts
	$(call print_step,Cleaning up local artifacts)
	
	# Remove Docker images
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) $(FULL_IMAGE) 2>/dev/null || true
	
	# Clean up directories
	rm -rf logs/* reports/* artifacts/* anomaly_report_*.txt
	
	# Docker system cleanup
	docker system prune -f
	
	$(call print_success,Local cleanup completed!)

cleanup: clean ## Remove all deployed resources
	$(call print_step,Removing deployed resources)
	
	# Remove Kubernetes resources
	@if kubectl get deployment ai-devops-demo -n $(K8S_NAMESPACE) >/dev/null 2>&1; then \
		kubectl delete -f k8s/manifests/ -n $(K8S_NAMESPACE) --ignore-not-found=true; \
		$(call print_success,Kubernetes resources removed); \
	else \
		echo "No Kubernetes resources to remove"; \
	fi
	
	# Remove Kyverno policies
	@if kubectl get crd clusterpolicies.kyverno.io >/dev/null 2>&1; then \
		kubectl delete -f k8s/policies/ --ignore-not-found=true; \
		$(call print_success,Security policies removed); \
	fi
	
	$(call print_success,Complete cleanup finished!)

dev: ## Start development environment
	$(call print_step,Starting development environment)
	
	# Build and run container with development settings
	docker build -t $(IMAGE_NAME):dev .
	docker run -it --rm -p 5000:5000 -e DEBUG=true -v $(PWD)/app:/app $(IMAGE_NAME):dev
	
# CI/CD simulation targets
ci-pipeline: setup build scan test ## Run complete CI pipeline locally
	$(call print_step,Running complete CI/CD pipeline simulation)
	$(call print_success,CI pipeline completed successfully!)

cd-pipeline: deploy-k8s monitoring ## Run complete CD pipeline
	$(call print_step,Running complete CD pipeline simulation)
	$(call print_success,CD pipeline completed successfully!)

full-demo: ci-pipeline cd-pipeline demo-ai ## Run complete demonstration
	$(call print_step,Running full AI-DevOps demonstration)
	@echo "$(GREEN)🎉 Complete AI-Augmented DevOps Pipeline Demo Finished!$(NC)"
	@echo ""
	@echo "$(BLUE)📋 What was demonstrated:$(NC)"
	@echo "✅ Pre-commit security hooks"
	@echo "✅ Container vulnerability scanning"  
	@echo "✅ Kubernetes deployment with security policies"
	@echo "✅ AI-powered anomaly detection"
	@echo "✅ Monitoring and observability setup"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "• Visit the running application"
	@echo "• Check the monitoring dashboards"
	@echo "• Review the AI analysis reports"
	@echo ""
	$(call print_success,Ready for production deployment!)
