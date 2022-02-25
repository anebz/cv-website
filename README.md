# Cloud challenge

Using AWS SAM

To deploy template to stack:

```bash
sam build
sam deploy
```
Upload index and website files to bucket

```bash
aws s3 cp static/. s3://anebz-cv/ --recursive
```
