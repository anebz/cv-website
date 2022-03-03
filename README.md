# Cloud challenge

Using AWS SAM

To deploy template to stack:

```bash
sam build
sam deploy
```
Upload index and website files to bucket

```bash
aws s3 cp static/. s3://anebz/ --recursive
```

Removing front-end resources from template because some things can't be done via code:

1. **S3**: create bucket and upload files (via template)
2. **Route 53**: create domain, which creates hosted zone
   1. We will need A type route and CNAME type route
3. **Certificate Manager**: create certificate for domain
   1. Request public certificate: SSL/TLS
   2. Select domain
   3. DNS validation
   4. When the certificate says: pending approval or similar, click on the create Record on Route 53. This will create CNAME route
4. **Cloudfront distribution**: create distribution
   1. Origin domain: select the S3 suggestion but instead of BUCKETNAME.s3.REGION.amazonaws.com, change it to BUCKETNAME.s3-website.REGION.amazonaws.com
   2. Viewer protocol policy: Redirect HTTP to HTTPS
   3. Alternate domain name (CNAME): add the domain name
   4. Custom SSL certificate: add the certificate from the suggestions
   5. Leave HTTP/s enabled
   6. Leave IPv6 On
   7. Create, it takes some minutes to deploy
5. Go to the domain name and you should see that the website has HTTPS
