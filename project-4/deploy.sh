#!/usr/bin/env bash

# Algorithm
## 0. Check if required variables are mapped, if not, ask to user

if [ -z $PROJECT_NAME ]
then
  # shellcheck disable=SC2034
  read -rp "Set the name of your project: " PROJECT_NAME
fi

if [ -z $AWS_ACCESS_KEY_ID ]
then
  # shellcheck disable=SC2034
  read -rp "Inform the AWS_ACCESS_KEY_ID: " aws_access_key_id
  export AWS_ACCESS_KEY_ID=$aws_access_key_id
fi

if [ -z $AWS_SECRET_ACCESS_KEY ]
then
  # shellcheck disable=SC2034
  read -rsp "Inform the AWS_SECRET_ACCESS_KEY: " aws_secret_acess_key
  export AWS_SECRET_ACCESS_KEY=$aws_secret_acess_key
fi

if [ -z $AWS_SESSION_TOKEN ]
then
  # shellcheck disable=SC2034
  read -rsp "Inform the AWS_SESSION_TOKEN: " aws_session_token
  export AWS_SESSION_TOKEN=$aws_session_token
fi

if [ -z $AWS_DEFAULT_REGION ]
then
  # shellcheck disable=SC2034
  read -rp "Inform the AWS_DEFAULT_REGION: " aws_default_region
  export AWS_DEFAULT_REGION=$aws_default_region
fi

if [ -z $AWS_ACCOUNT ]
then
  # shellcheck disable=SC2034
  read -rp "Inform the AWS_ACCOUNT_ID: " aws_account
  export AWS_ACCOUNT=$aws_account
fi


## 1. Run Terraform
echo "\nExecuting terraform"
cd terraform/ || exit
terraform init
terraform apply -var "project_name=$PROJECT_NAME" -auto-approve -auto-approve
cd ..

echo "\nDone creating assets!"

## 2. Upload emr files to s3
echo "\nUploading files to EMR bucket"

# shellcheck disable=SC2116
# shellcheck disable=SC2046
S3_EMR_BUCKET=$(echo "s3://"$(aws s3 ls | grep "$PROJECT_NAME"-emr | cut -c 21-))

echo "\nUploading bootstrap_actions script: install_packages.sh"
aws s3 cp $(pwd)/emr/install_packages.sh $S3_EMR_BUCKET/bootstrap_actions/install_packages.sh

echo "\nUploading job_template.py"
aws s3 cp $(pwd)/emr/job_template.py $S3_EMR_BUCKET/src/job_template.py

echo "\nZipping packages directory"
cd emr/ || exit
zip -r $(pwd)/packages.zip packages/
cd ..

echo "\nUploading packages.zip"
aws s3 cp $(pwd)/emr/packages.zip $S3_EMR_BUCKET/packages/packages.zip

echo "\nRemoving packages.zip"
rm $(pwd)/emr/packages.zip

## 3. Build Image and push to ECR
echo "\nBuilding image and pushing to ECR"

echo "\nBuilding image"
docker build --rm -t $PROJECT_NAME:\latest .

echo "\nLogin in ecr"
# shellcheck disable=SC2046
eval $(aws ecr get-login-password)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com

echo "\nTagging (as latest) and pushing image to ECR"
docker tag $PROJECT_NAME $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$PROJECT_NAME:\latest
docker push $AWS_ACCOUNT.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$PROJECT_NAME:\latest