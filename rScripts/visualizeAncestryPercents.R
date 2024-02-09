library(tidyverse)
library(RColorBrewer)

#Read in data
data <- read.table("results/quantifyRepresentation/race.tsv", header = FALSE, sep = "\t", col.names = c("AncestralGroup", "Count"))
categories <- c("European", "African", "Hispanic/Latin American", "Asian", "Multiple Ancestry", "Greater Middle Eastern", "Native American", "Oceanian")
print(data)
#Get percentages
data$Percentage <- (data$Count / sum(data$Count)) * 100
#Change Ancestral group numbers to strings from categories list
data$AncestralGroup <- factor(data$AncestralGroup, labels = categories)

#plot (bar graph)
plot <-ggplot(data, aes(x = reorder(AncestralGroup, -Percentage), y = Percentage, fill = AncestralGroup)) +
  geom_bar(stat = "identity", fill = c("#1f78b4ff","#fe7f0e", "#2ba02d", "#d52728", "#8c5749", "#e178c0", "#7d7d7d", "#b4b344") ) +
  geom_text(aes(label = paste0(round(Percentage, 2), "%")),
            position = position_dodge(width = 0.9),
            vjust = -0.25,
            size = 5,
            color = "black") +
  theme_minimal() +
  labs(title = "Percent of Transcriptomic Samples by Ancestry",
       x = "Ancestral Group",
       y = "Percentage (%)") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 15), plot.title = element_text(hjust = 0.5, size = 25), axis.text.y = element_text(size = 15),axis.title.x = element_text(size = 15), axis.title.y = element_text(size = 15))
ggsave("results/quantifyRepresentation/ancestral_groups_percentage.png", plot, width = 10, height = 8, dpi = 300)
print('functional')