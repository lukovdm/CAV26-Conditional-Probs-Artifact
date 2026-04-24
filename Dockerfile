FROM lukovdm/paynt:cav26

RUN apt-get install texlive-full -y

WORKDIR /opt/benchmarks

# Copy requirements
COPY requirements.txt .

# Install extra dependencies for benchmarks
RUN pip install -r requirements.txt

# Copy other files
COPY . .

# Start jupyter lab
CMD ["jupyter", "lab", "--ip=0.0.0.0"]
