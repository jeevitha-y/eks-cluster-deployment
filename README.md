# Amazon EKS Cluster Deployment

## Overview

This project demonstrates the deployment of a containerized Python game application on **Amazon Elastic Kubernetes Service (EKS)** using **AWS Fargate**. The application container image is stored in **Amazon ECR Public** and exposed to the internet through an **AWS Application Load Balancer (ALB)** using the **AWS Load Balancer Controller**.

---

## Architecture

```text
Python Game Application
        │
        ▼
Docker Build
        │
        ▼
Amazon ECR Public
        │
        ▼
Amazon EKS (AWS Fargate)
        │
        ▼
Kubernetes Deployment
        │
        ▼
Kubernetes Service
        │
        ▼
Kubernetes Ingress
        │
        ▼
AWS Load Balancer Controller
        │
        ▼
Application Load Balancer (ALB)
        │
        ▼
Browser
```

---

## Technologies Used

* Amazon EKS
* AWS Fargate
* Amazon ECR Public
* Docker
* Kubernetes
* kubectl
* eksctl
* Helm
* AWS IAM
* AWS Load Balancer Controller
* Application Load Balancer (ALB)
* Python (Flask)

---

## Prerequisites

Install the following tools before starting:

* AWS CLI
* Docker
* kubectl
* eksctl
* Helm
* AWS Account

---

# Deployment Steps

## 1. Create an Amazon EKS Cluster

```bash
eksctl create cluster \
  --name demo-cluster \
  --region us-east-1 \
  --fargate
```

---

## 2. Configure kubectl

```bash
aws eks update-kubeconfig \
  --region us-east-1 \
  --name demo-cluster
```

---

## 3. Create a Fargate Profile

```bash
eksctl create fargateprofile \
  --cluster demo-cluster \
  --region us-east-1 \
  --name alb-sample-app \
  --namespace game-app
```

---

## 4. Associate the IAM OIDC Provider

```bash
export cluster_name=demo-cluster

eksctl utils associate-iam-oidc-provider \
  --cluster $cluster_name \
  --approve
```

---

## 5. Download the IAM Policy

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.11.0/docs/install/iam_policy.json
```

---

## 6. Create the IAM Policy

```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

---

## 7. Create the IAM Service Account

Replace `<AWS_ACCOUNT_ID>` with your AWS Account ID.

```bash
eksctl create iamserviceaccount \
  --cluster=demo-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::<AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```

---

## 8. Install the AWS Load Balancer Controller

Add the Helm repository:

```bash
helm repo add eks https://aws.github.io/eks-charts

helm repo update
```

Install the controller:

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=demo-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=us-east-1 \
  --set vpcId=<YOUR_VPC_ID>
```

---

## 9. Verify the Controller

```bash
kubectl get deployment -n kube-system aws-load-balancer-controller

kubectl get pods -n kube-system
```

---

## 10. Deploy the Application

```bash
kubectl apply -f game_full.yaml
```

or directly from GitHub:

```bash
kubectl apply -f https://raw.githubusercontent.com/jeevitha-y/eks-cluster-deployment/main/game_full.yaml
```

---

## 11. Verify the Deployment

```bash
kubectl get all -n game-app
```

Check the Ingress:

```bash
kubectl get ingress -n game-app
```

Once the Application Load Balancer is provisioned, the **ADDRESS** column will display the ALB DNS endpoint.

---

# Project Structure

```text
eks-cluster-deployment/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── game_full.yaml
└── README.md
```

---

# Kubernetes Resources

The project deploys the following Kubernetes resources:

* Namespace
* Deployment
* Service
* Ingress

---

# Container Image

The application image is stored in Amazon ECR Public.

```text
public.ecr.aws/<your-public-alias>/game-app:v1
```

Update the Deployment manifest with your public image URI if required.

---

# Features

* Deploys a containerized Python application on Amazon EKS.
* Uses AWS Fargate for serverless Kubernetes compute.
* Stores container images in Amazon ECR Public.
* Uses Kubernetes Deployment for application management.
* Exposes the application through a Kubernetes Service.
* Uses Kubernetes Ingress with the AWS Load Balancer Controller.
* Automatically provisions an internet-facing AWS Application Load Balancer.

---

# Cleanup

Delete the Kubernetes resources:

```bash
kubectl delete -f game_full.yaml
```

Delete the EKS cluster:

```bash
eksctl delete cluster \
  --name demo-cluster \
  --region us-east-1
```

---

# Learning Outcomes

Through this project, I learned how to:

* Build and containerize a Python application using Docker.
* Store container images in Amazon ECR Public.
* Create and manage an Amazon EKS cluster with AWS Fargate.
* Configure IAM OIDC Provider and IAM Service Accounts.
* Install and configure the AWS Load Balancer Controller using Helm.
* Deploy Kubernetes workloads using Deployments, Services, and Ingress.
* Expose applications through an AWS Application Load Balancer (ALB).
* Manage Kubernetes resources using `kubectl`.
