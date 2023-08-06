# Prompt Pilot

*DISCLAIMER: It's currently in development and I am uploading this primarily as a placeholder with some functions that you guys can play around with.*

Prompt Pilot is a prompt engineering library for AI models that introduces the concept of "prompt functions" to improve the process of prompt engineering by allowing developers to create complex prompts with just one function.

Example:

```
marketing_analyst(name="Sarah", company_name="ABC Corp", company_industry="E-commerce")
```

This will return a a string object with a detailed set of instructions for the marketing analyst bot that can be passed in as an argument in API call scripts to AI model providers such as OpenAI / Replicate etc.
