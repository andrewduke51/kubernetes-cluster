FROM tiangolo/uwsgi-nginx-flask:python3.10

ARG USERNAME=default-user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
RUN export PATH="$HOME/.local/bin:$PATH"
COPY app/requirements.txt /app/requirements.txt
RUN pip install --user --no-cache-dir --upgrade -r /app/requirements.txt


COPY ./app /app
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD ["main.py"]