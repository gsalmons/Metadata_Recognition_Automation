library(tidyverse)
library(RColorBrewer)

#Read in data
data <- read.table("results/quantifyRepresentation/sex.tsv", header = TRUE, sep = "\t", col.names = c("BiologicalSexGroup", "Count"))
categories <- c("Female", "Male")
print(data)
#Get percentages
data$Percentage <- (data$Count / sum(data$Count)) * 100
#Change sex group numbers to strings from categories list
data$BiologicalSexGroup <- factor(data$BiologicalSexGroup, levels = unique(data$BiologicalSexGroup), labels = categories)

#plot (bar graph)
plot <-ggplot(data, aes(x = reorder(BiologicalSexGroup, -Percentage), y = Percentage)) +
  geom_bar(stat = "identity", fill = c("#1f78b4ff")) +
  geom_text(aes(label = paste0(round(Percentage, 2), "%")),
            position = position_dodge(width = 0.9),
            vjust = -0.25,
            size = 5,
            color = "black") +
  theme_minimal() +
  labs(title = "",
       x = "Biological Sex",
       y = "Percentage (%)") +
  theme_bw() +
  theme(axis.text.x = element_text(size = 25),
        axis.text.y = element_text(size = 15),
        strip.background = element_rect(colour = "white", fill = "white"),
        strip.text.x = element_text(size = 25),
        axis.title.x = element_text(size = 25),
        axis.title.y = element_text(size = 25),
        legend.position = "none") +
  scale_y_continuous(breaks = seq(0, 60, by = 20), limits = c(0, 60))
  # theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 15), plot.title = element_text(hjust = 0.5, size = 25), axis.text.y = element_text(size = 15),axis.title.x = element_text(size = 15), axis.title.y = element_text(size = 15))
ggsave("results/quantifyRepresentation/sex_groups_percentage.png", plot, width = 13, height = 6, dpi = 300)
print('functional')