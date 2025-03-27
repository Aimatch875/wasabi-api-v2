from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

@app.route('/generate-url', methods=['POST'])
def generate_url():
    try:
        data = request.get_json()
        bucket = data['bucket']
        key = data['key']
        expires_in = data.get('expiresIn', 3600)

        s3 = boto3.client(
            's3',
            endpoint_url='https://s3.us-east-1.wasabisys.com',
            aws_access_key_id=os.environ['WASABI_ACCESS_KEY'],
            aws_secret_access_key=os.environ['WASABI_SECRET_KEY'],
            region_name='us-east-1'
        )

        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )

        print(f"Generated Pre-signed URL: {url}")  # 🔍 debug
        return jsonify({'url': url}), 200

    except Exception as e:
        print(f"Error: {str(e)}")  # 🔍 debug
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
