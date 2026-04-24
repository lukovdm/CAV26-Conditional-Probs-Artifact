FROM lukovdm/paynt:cav26

RUN apt-get install texlive-full -y

RUN apt-get install parallel -y

WORKDIR /opt/benchmarks

# Copy requirements
COPY requirements.txt .

# Install extra dependencies for benchmarks
RUN pip install -r requirements.txt

# Copy other files
COPY . .

EXPOSE 8888

# Set default Jupyter token to "cav26"
RUN mkdir -p /root/.jupyter && \
    printf "c.ServerApp.token = 'cav26'\nc.ServerApp.password = ''\n" > /root/.jupyter/jupyter_server_config.py

# Start jupyter lab in the background, then drop into a bash shell
CMD ["bash", "-c", "jupyter lab --ip=0.0.0.0 --allow-root --no-browser > /var/log/jupyter.log 2>&1 & exec bash"]
