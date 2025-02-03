
FROM zenmldocker/zenml
COPY . /slmops
WORKDIR /slmops

RUN pip install uv
RUN uv pip install -e /slmops/packages/orchestration
RUN uv pip install -e /slmops/packages/ml
