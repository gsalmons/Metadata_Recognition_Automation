library(tidyverse)
library(RColorBrewer)

#Read in data
race_data <- read.table("results/quantifyRepresentation/race.tsv", header = FALSE, sep = "\t", col.names = c("Numbers", "Count"))
categories <- c("European", "African", "Hispanic/Latin American", "Asian", "Multiple Ancestry", "Greater Middle Eastern", "Native American", "Oceanian")
#Get percentages 
race_data$Percentage <- (race_data$Count / sum(race_data$Count)) * 100
#Change Ancestral group numbers to strings from categories list
race_data$Category <- factor(race_data$Numbers, levels = unique(race_data$Numbers), labels = categories)

#Read in data
sex_data <- read.table("results/quantifyRepresentation/sex.tsv", header = TRUE, sep = "\t", col.names = c("Numbers", "Count"))
sex_categories <- c("Female", "Male")
#Get percentages
sex_data$Percentage <- (sex_data$Count / sum(sex_data$Count)) * 100
#Change sex group numbers to strings from categories list
sex_data$Category <- factor(sex_data$Numbers, levels = unique(sex_data$Numbers), labels = sex_categories)

sex_data$CategoryType <- 'Sex'
race_data$CategoryType <- 'Race'
combined_data <- rbind(race_data, sex_data)
combined_data$CategoryType <- factor(combined_data$CategoryType, levels = c("Sex", "Race"))

color_mapping <- c('Sex' = "#1f78b4ff", 'Race' = "#fe7f0e")

plot <- ggplot(combined_data, aes(x = reorder(Category, -Percentage), y = Percentage, fill = CategoryType)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = paste0(round(Percentage, 2), "%")),
            position = position_dodge(width = 0.9),
            vjust = -0.25,
            size = 6,
            color = "black") +
  facet_wrap(~ CategoryType, scales = "free_x", ncol = 1) +
  scale_fill_manual(values = color_mapping) +
  theme_bw() +
  labs(x= "",
       y = "Percentage (%)") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 25),
        axis.text.y = element_text(size = 15),
        strip.background = element_rect(colour = "white", fill = "white"),
        strip.text.x = element_text(size = 25),
        axis.title.y = element_text(size = 25),
        legend.position = "none")

# Save the plot
ggsave("results/quantifyRepresentation/combined_groups_percentage.png", plot, width = 13, height = 17, dpi = 300)

print('Plot created')