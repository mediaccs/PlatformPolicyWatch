## To cite this tool:
Chan, N. K., Su, C. C., & Shore, A. (2023). Shifting platform values in community guidelines: Examining the evolution of TikTok’s governance frameworks. New Media & Society. Advance online publication. https://doi.org/10.1177/14614448231189476

# Platform Policy Watch 
## A Tool for Archiving and Analyzing Policy Changes in Platform Governance

## Introduction

Platform policies, such as Terms of Service (ToS), community guidelines, and privacy policies, are instrumental in setting standardized rules for digital platforms. Scholars emphasize the importance of studying platform governance frameworks, which offer idealized accounts of platform identity and governance principles. However, longitudinal studies of platform policies are rare in communication research due to challenges like corporate secrecy and the lack of historical records. To address this gap, we present the Platform Policy Watch tool. This tool aims to systematically collect, analyze, and document platform policies, providing a methodological framework for studying platform histories.

*Please acknowledge this repository by citing it if you decide to use our tool.*
## To cite this tool:
Chan, N. K., Su, C. C., & Shore, A. (2023). Shifting platform values in community guidelines: Examining the evolution of TikTok’s governance frameworks. New Media & Society. Advanced online publication. https://doi.org/10.1177/14614448231189476

## Overview of the Tool

Our tool comprises three components:

1. [**PolicyTimeMachine:**](https://github.com/mediaccs/PlatformPolicyWatch/tree/main/PolicyTimeMachine) This component is responsible for scraping and tracking platform policies from various sources, including historical policy scraping from the Wayback Machine and recording the latest policies from official platforms.

2. [**PolicyParser:**](https://github.com/mediaccs/PlatformPolicyWatch/tree/main/PolicyParser) Designed to clean and segment the collected policies into distinct sections for further data analysis.

3. [**PolicyLabeler:**](https://github.com/mediaccs/PlatformPolicyWatch/tree/main/PolicyLabeler) Utilizes ChatGPT to code the segmented data, streamlining the coding process.

With this tool, researchers can explore the evolution of platform policies and the methodological challenges involved in longitudinal research.

#### Overview of Platform Policy Watch 
<img width="377" alt="framework" src="https://github.com/mediaccs/PlatformPolicyWatch/assets/11847478/e6224907-ff71-4b24-9c21-136862419c68">

## Component 1 - PolicyTimeMachine: Scraping and Tracking of Platform Policies

We've developed a custom Python program named PolicyTimeMachine for tracking policies on approximately 50 social media and labor platforms. It consists of two main functions:

### Function 1: Historical Policy Scraping

This function retrieves data from the Wayback Machine, an archive containing billions of web pages stored chronologically. Our program modifies the URL's date and target address to generate a list of all archived target pages. It accesses these URLs, storing relevant data in structured Comma-Separated Values (CSV) files for future analysis.

### Function 2: Latest Policy Recording

This function directly extracts the latest policies from platforms' official sites, saving them in the same CSV format.

## Component 2 - PolicyParser: Segmenting Platform Policies

PolicyParser is designed to segment collected policies into distinct sections for data analysis. These sections help in addressing specific subjects, situations, or aspects related to platform usage, application, and content production.

## Component 3 - PolicyLabeler: Labeling and Coding Platform Policies

PolicyLabeler automates the labeling of extracted policy sections based on ChatGPT's large language models by sending queries to the OpenAI API. This Python-based program enables researchers to extract codes, such as values, actors, and responsibilities, from platform policies. It involves setting up the environment, obtaining OpenAI's API Key, preparing prompts, running models, and potential fine-tuning based on accuracy and performance.

## Conclusion

The Platform Policy Watch tool empowers researchers to systematically document and analyze platform governance changes. It can help in triangulating narratives of platform histories with platforms' and users' perspectives. However, it's essential to recognize that research tools involve invisible work, especially during moments of breakdown. We advocate for a more reflexive approach to computational research tools, allowing communication researchers to adapt tools to their research and critically assess their methodological strengths and weaknesses.

*Feel free to adjust, modify, and add any additional information based on the study context to effectively use this tool.*
