library(tidyverse)
library(RColorBrewer)

#Read in data
data <- read.table("results/quantifyRepresentation/race.tsv", header = FALSE, sep = "\t", col.names = c("AncestralGroup", "Count"))

data <- data %>% 
  filter(!AncestralGroup %in% c(0, 9))
print(data)
categories <- c("European", "African", "Hispanic/Latin American", "Asian", "Multiple Ancestry", "Greater Middle Eastern", "Native American", "Oceanian")

print(data)
#Get percentages
data$Percentage <- (data$Count / sum(data$Count)) * 100
#Change Ancestral group numbers to strings from categories list
data$AncestralGroup <- factor(data$AncestralGroup, labels = categories)

#plot (bar graph)
plot <-ggplot(data, aes(x = reorder(AncestralGroup, -Percentage), y = Percentage)) +
  geom_bar(stat = "identity", fill = c("#c28d80")) + # "#fe7f0e"
  geom_text(aes(label = paste0(round(Percentage, 2), "%")),
            position = position_dodge(width = 0.9),
            vjust = -0.25,
            size = 5,
            color = "black") +
  theme_minimal() +
  labs(title = "",
       x = "Ancestry",
       y = "Percentage (%)") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 25),
        axis.text.y = element_text(size = 15),
        strip.background = element_rect(colour = "white", fill = "white"),
        strip.text.x = element_text(size = 25),
        axis.title.x = element_text(size = 25),
        axis.title.y = element_text(size = 25),
        legend.position = "none")
  # theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 15), axis.text.y = element_text(size = 15),axis.title.x = element_text(size = 15), axis.title.y = element_text(size = 15))
ggsave("results/quantifyRepresentation/ancestral_groups_percentagePink.png", plot, width = 13, height = 9.5, dpi = 300)
print('functional')