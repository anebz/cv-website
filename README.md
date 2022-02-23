# Cloud challenge

To deploy dynamodb stack:

```bash
aws cloudformation deploy --template-file dynamodb.yaml --stack-name static-website --capabilities  CAPABILITY_NAMED_IAM
```

Upload index and website files to bucket

```bash
aws s3 cp static/. s3://anebz-cv2/ --recursive
```

