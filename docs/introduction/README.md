---
icon: house
---

# Welcome to LMOrbits

Welcome to LMOrbits! We are thrilled to introduce you to this amazing package designed for operating the small language models. Here, you'll find a clear structure to help you get started, along with detailed information about the project and its components. We can't wait for you to explore everything we have to offer and embark on your journey into the fascinating world of language models!


## Project Structure

To kick off your journey with our project, let's break it down into three exciting Git repositories! First up, we have the **Infrastructure as Code (IaC)** repository, which lays the groundwork for our infrastructure. Next, we dive into the **Operations** repository, where the magic happens as we manage and orchestrate our workflows. Finally, we have the **Application** repository, where you can find the application that utilizes the models in a tailored manner.

you can explore each of these core repositories one by one, as it contains the essential packages that power the entire logic of our project. Get ready to discover the building blocks of LMOrbits and how they come together to create a seamless experience!

1. **Lmorbits**
   - [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Parsa-Mir/lmorbits)
   - This repository manages all the logic for our operations.

2. **Infrastructure as Code (IaC)**
   - [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Parsa-Mir/slmops_infra)
   - This repository lays the groundwork for our infrastructure.</br>
 {% hint style="success" %} Accessible within the lmorbits repository. {% endhint %}

3. **Serve**
   - [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Parsa-Mir/serve)
   - This repository is where the effort to make the serving model based on the experiment tracker easier specially on the user side.</br>
   {% hint style="success" %} Accessible within the lmorbits repository. {% endhint %}

4. **Application**
   - [![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Parsa-Mir/slmops-app)
   - This repository showcases a full stack application with LMOrbits integration.</br>
     {% hint style="warning" %} Not accessible within the LMOrbits repository. {% endhint %}

### IaC

Our infrastructure is designed to seamlessly support both cloud and local environments, making it versatile and user-friendly! For on-prem/local development, we utilize K3D/k3s, which allows you to easily set up a a light weight local Kubernetes environment on your system. This means you can test and develop the package  right from your machine/machines! However, some functionalities, such as using cloud GPUs, may not work in this setup unless you have GPUs available in the K3s or K3D cluster.

On the cloud side, we leverage Terraform to manage our infrastructure instances efficiently. Our primary focus is on Google Cloud and Civo, where we implement various modules, including IAM rules, to ensure secure access and management. We cover essential services such as Google Cloud Storage, Vertex AI, Virtual Private Cloud (VPC), service accounts, compute resources, Cloud Build, and the Artifact Registry.

Additionally, we support three distinct environments to cater to different stages of development. For Kubernetes system implementation, we use SIBO, which helps us initiate and manage cloud-native solutions effectively. This robust setup empowers you to build and deploy applications with confidence, whether locally or in the cloud!

### LMOrbits
LMOrbits focuses on the dynamic management and operation of Small Language Models (SLMs) through five interconnected components: Applications, which enable the creation of innovative SLM-based solutions; APP, which is the orchestration around the usage of the SLM such as chains, agents, vectordb and tools; Data, which provides a robust framework for data tasks; ML, where model fine-tuning, evaluations, and experiment tracking , quantization, distilations occur; Orchestration, powered by ZenML, that manages workflows across development, production, and staging; and Serve, responsible for deploying models in various environments. Together, these packages facilitate effective collaboration and enhance the overall functionality of the system, allowing users to explore the vast potential of LMOrbits.


## Need Help?

- 📝 Open an issue in our GitHub repository
- 💬 Join our community Discord
- 📧 Contact support@example.com 