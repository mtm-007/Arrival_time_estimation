FROM python:3.12-slim 

RUN pip install pipenv 

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["predict.py", "model_linear_reg_w_PU_DO.bin", "./"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]