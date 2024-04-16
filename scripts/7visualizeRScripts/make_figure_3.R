#Display the AUC-PR curves for sex, ancestry, and tumor_stage
library(precrec)
library(ggplot2)

# Assuming you have vectors ytrue and scores
ytrue <- c(1, 0, 1, 1, 0) # True binary labels
scores <- c(0.9, 0.4, 0.6, 0.8, 0.3) # Predicted scores or probabilities

# Calculate AUC-PR
aucpr <- evalmod(scores = scores, labels = ytrue, mode = "basic")

# Plot PR curve
autoplot(aucpr) + theme_minimal() +
  ggtitle("Precision-Recall Curve") +
  xlab("Recall") + ylab("Precision") +
  theme(plot.title = element_text(hjust = 0.5))

# To print AUC-PR value
print(aucpr@auc.integral)

# Note: The actual plotting and calculation lines might slightly vary based on your specific requirements and data.