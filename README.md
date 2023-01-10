# Seazone Code Challenge - APIs Back End
[Descrição](seazone_code_challenge_2.pdf)

## Pre-requisitos
 * Python >= 3.8.8 
 * PostgreSQL (ou usar o sqlite)
 * Criar ``.env`` (se for usar PostgreSQL, exemplo ``.env.exemple``)

## Setup
### 1 - **Criar ambiente virtual env**

- #### Windows
```bash
#instalar virtual-env
pip install virtualenv

# criar ambiente venv
python -m venv venv

#ativar ambiente Virtual
.\venv\Scripts\activate
```
- #### Linux Unbutu

```bash
#instalar virtual-env
sudo pip3 install virtualenv


# criar ambiente venv
python3 -m venv venv

#ativar ambiente Virtual
source venv/bin/activate
```

### 2 - **Instalar as dependencias**

- #### Windows
```bash
pip install -r requirements.txt
```
- #### Linux Unbutu
```bash
pip3 install -r requirements.txt
```

## Start Projeto:

### **Migrate**
- #### Windows
```shell
python .\manage.py migrate
```
- #### Linux Unbutu
```shell
python3 manage.py migrate
```

### **Start**

- #### Windows
```shell
python .\manage.py runserver
```
- #### Linux Unbutu
```shell
python3 manage.py runserver
```
## Tests:
- #### Windows
```shell
python .\manage.py test
```
- #### Linux Unbutu
```shell
python3 manage.py test
```