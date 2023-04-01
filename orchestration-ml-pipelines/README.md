# Workflow Orchestration

It's a set of facilities/tools that schedule a number of steps/stages to be accomplished, e.g.,  Scheduling ML models training

Exmaple pipeline: 
```
CSV -> Pandas -> xgboost -> mlflow
       Pandas -> Postgres -> TALEND -> ElasticSearch -> Kibana
```
Random Points of Failure can occur in the pipeline. The goal of the workflow orchestration is to minimize the errors and fail
gracefully.

In more interconnected pipelines (Different pipelines interconnected), there is a need to handle cases where common components fail and how this will affect the data flow
and processing of the data.

# Negative Engineering
90% of data engineers time is spent on avoiding negative scenarios from happening:
+ Retries of APIs failure
+ handling Malformed data
+ building Notification facilities
+ Conditional Failure Logic
+ Timeouts

```
Prefect workflow orchestration framework was built with the mission of reducing the impact of negative engineering by 
reducing the time spent on that from 90% to 20%, allowing data scientists to focus on improving the model and its performance.
```



# Introducing Prefect:
Open Source Workflow Orchestration Framework for eliminating Negative Engineering:
+ Open Source
+ Python-based
+ Native Dask integration  (you can run your task on top of Dask)
+ Very active Community  (> 10k Github star)
+ Prefect Cloud/Prefect Server

Prefect Orion (aka Prefect 2.0) has a substantial improvement over Prefect 1.0 to support the dynamic and scalable workloads  of the modern data stack.


With the help of its new asynchronous engine, Prefect offers a simple approach to convert any function into a unit of work that can be monitored and managed through orchestration regulations.

It allows you to include workflow features such as distributed execution, scheduling, caching, retries, and many others to your code with minimal modifications. Furthermore, every activity is recorded and can be viewed in the Prefect server or Prefect Cloud dashboard.


```python
from prefect import flow, task
from typing import List
import httpx


@task(retries=3)
def get_stars(repo: str):
    url = f"https://api.github.com/repos/{repo}"
    count = httpx.get(url).json()["stargazers_count"]
    print(f"{repo} has {count} stars!")


@flow(name="GitHub Stars")
def github_stars(repos: List[str]):
    for repo in repos:
        get_stars(repo)


# run the flow!
github_stars(["PrefectHQ/Prefect"])
```


# Exercise:

You know, we cannot deploy a jupitor notebook in order to use it along with Prefect for workflow orchestration. Instead, and after designing and implementing the script using notebook, we need to convert the code into a normal python script.

To prepare the code for this workflow orchestration task, you need to do the following:
 * create a new `model_building.py` script file under your project
 * copy the code from the notebook () into this `model_building.py`. 
 * make sure to omit any plotting code segments
 * make sure to have at least two functions so that we can properly unit test them in the future and to attach observability facility to eqach function: 
   * one for data preparation
   * the other for building the model

* add the `main` function then call the functions that prepares the training data and builds the model.



## Adding a  Prefect flow:

 * We include and utilize Prefect in our code by wrapping the workflow function (e.g., the main function in our case), which retrieves, preprocesses, vectorizes the data, and trains the model with a `@flow` decorator as:

```python
from prefect import flow

@flow
def main():
  ...
```
 * This leads to extra logging as you will see on the console. The main workflow function is what is usually put in a `if "__name"" == "__main__":` block.

 * Multiple Flows can be put in the same file.

## Adding a Prefect task:


Tasks are added by using the `@task` decorator around our task function (example: preprocessing, training... etc):
```python
@task
def train_the_model(X,y):
  ...
```


```python
from prefect import flow, task

X_train, X_val, y_train, y_val, dv = getPreprocessedData (traing_data, test_data ):
```

Adding a task enables further logging.

Tasks can also have parameters like caching and retries.


# Deployment using Prefect

Deployment in Prefect refers to the process of taking the workflow that has been created and making it available for execution on a remote environment.

There are several deployment options available in Prefect, including:

 * Local: This is the simplest deployment option, where the workflow is executed on the user's local machine. This is useful for testing and development purposes, but not recommended for production use.

 * Prefect Cloud: This is a hosted service provided by Prefect that allows users to deploy and run workflows in the cloud. It provides a fully managed environment with scalability, reliability, and security features.

 * Self-hosted: Users can deploy Prefect on their own infrastructure, such as on-premise or on a private cloud. This provides greater control over the deployment environment, but requires more setup and maintenance.

To deploy a workflow in Prefect, the user first needs to create a project and define the workflow using the Prefect API or the Prefect Flow syntax. Once the workflow is defined, it can be deployed to the desired deployment environment using Prefect CLI or the Prefect UI.

## Practice: Deployment using Prefect in action
 * Assume have a simple project to preprocess sales data stored in csv file by removing rows with null values. orchestration-ml-pipelines\basic-demo
 * The script contains a prefect flow along with Prefect tasks.
 * First, we need to create a yaml file that contains the deployment configurations using the command:
   * demo-deployment-sales: deployment name
   * prefect-demo.py: script file containing the Prefect flow and tasks 
   * main_flow_sales: entry points referring to the function decorated with @flow
```python
 prefect deployment build --name demo-deployment-sales prefect-demo.py:main_flow_sales
```
* After running the above command the yaml file will be created and stored into the working directory
* Now, we need to create the deployment by running the following command and passing the yaml file.
```python
 prefect deployment apply main_flow_sales-deployment.yaml
```
* Each Deployment is associated with exaclty one flow under perfect. That means, you can trigger and schedule flow runs from this deployment.
* Such flow runs will be queued for execution by an `agent`. The agent listens for runs and execute the ones on their scheduled time.





