from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

# Hugging Face model 1 → will generate the short notes
llm = HuggingFaceEndpoint(
    model="meta-llama/Llama-3.1-8B-Instruct",
    task="conversational",
    provider="featherless-ai",
)

model1 = ChatHuggingFace(llm=llm)

# Hugging Face model 2 → will generate Q&A and merge the final output
# Same HuggingFaceEndpoint / ChatHuggingFace concept as above.
llm2 = HuggingFaceEndpoint(
    model="Qwen/Qwen2.5-7B-Instruct",
    task="conversational",
    provider="featherless-ai"
)

model2 = ChatHuggingFace(llm=llm2)


prompt1 = PromptTemplate(
    template="Generate a Short and concise notes from the following text \n {text}",
    input_variables=["text"],
)

prompt2 = PromptTemplate(
    template="Generate total 3 short questions answers from following notes \n {text}",
    input_variables=["text"],
)

prompt3 = PromptTemplate(
    # IMPORTANT: variable names must match input_variables.
    # {notes} and {que_ans} will come from RunnableParallel's output.
    template="Merge the provided notes and q&a into a single document \n notes -> {notes} \n q&a -> {que_ans}",
    input_variables=["notes", "que_ans"],
)

parser = StrOutputParser()


# NEW: RunnableParallel
# Both branches receive the SAME input at the same time.
#
# Input:
#     {"text": original_text}
#
#                 ┌─ prompt1 → model1 → parser → "notes"
# original text ──┤
#                 └─ prompt2 → model2 → parser → "que_ans"
#
# Output becomes:
# {
#     "notes": "...",
#     "que_ans": "..."
# }
parallel_chain = RunnableParallel(
    {
        "notes": prompt1 | model1 | parser,
        "que_ans": prompt2 | model2 | parser
    }
)


# This receives the dictionary produced by parallel_chain.
#
# {notes, que_ans}
#       ↓
#     prompt3
#       ↓
#     model2
#       ↓
#     parser
#       ↓
# final merged document
merge_chain = prompt3 | model2 | parser


# First run the parallel branches,
# then send their combined output into merge_chain.
chain = parallel_chain | merge_chain


result = chain.invoke(
    {
    "text": """SVM (Support Vector Machine) is a supervised machine learning algorithm mainly used for classification and regression tasks. The main objective of SVM is to find the best decision boundary, called a hyperplane, that separates data points belonging to different classes. SVM tries to choose the hyperplane in such a way that the distance between the hyperplane and the nearest data points from each class is as large as possible. This distance is called the margin. The data points that are closest to the decision boundary are known as Support Vectors because they play an important role in determining the position of the hyperplane.

    SVM can be used for both linearly and non-linearly separable data. For non-linear problems, SVM uses a technique called the Kernel Trick, which allows the algorithm to work in a higher-dimensional feature space without explicitly transforming the data. Common kernels available in scikit-learn are linear, polynomial (poly), radial basis function (rbf), and sigmoid. The RBF kernel is commonly used when the relationship between features and classes is non-linear.

    In scikit-learn, SVC (Support Vector Classifier) is used for classification and SVR (Support Vector Regression) is used for regression. Some important parameters of SVC are C, kernel, and gamma. The C parameter controls how strongly the model penalizes misclassified training examples. A high value of C tries to classify the training data more accurately, while a lower value allows a wider margin with some classification errors. The gamma parameter controls how much influence a single training example has when using kernels such as RBF. Feature scaling is generally important when using SVM because SVM is sensitive to the scale of the input features.

    Example:
    from sklearn.svm import SVC

    model = SVC(kernel="linear", C=1.0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    Overall, SVM is a powerful algorithm that works well for classification problems, especially when the number of features is large. Its main concepts are hyperplane, margin, support vectors, kernels, and regularization through the C parameter.
    """
    }
)

print(result)

# Visualize the complete Runnable graph.
# It does NOT execute the chain; it only shows the workflow structure.
chain.get_graph().print_ascii()