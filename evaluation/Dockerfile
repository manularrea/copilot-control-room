FROM python:3.12-slim
WORKDIR /verifier
COPY evaluation/verify.py /verifier/verify.py
USER 65534:65534
ENTRYPOINT ["python", "-I", "-B", "/verifier/verify.py", "--candidate", "/candidate"]
