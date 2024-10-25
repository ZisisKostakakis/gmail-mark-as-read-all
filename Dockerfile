FROM public.ecr.aws/lambda/python:3.9

COPY ./gmail_read_all_emails.py ${LAMBDA_TASK_ROOT}
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip3 install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

CMD ["gmail_read_all_emails.lambda_handler"]