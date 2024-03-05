library(tidyverse)
data <- read.csv("results/Thresholds.tsv", header=TRUE,sep="\t")
print(data)
data_long <- tidyr::pivot_longer(data, cols = -Threshold, names_to = "PrecisionType", values_to = "Precision")

# ggplot(data_long, aes(x = Threshold, y = Precision, colour = PrecisionType, group = PrecisionType)) + 
#   geom_line(size = 1) + 
#   geom_point(aes(shape = PrecisionType), size = 2) + # Points' shape depends on PrecisionType
#   geom_vline(xintercept = 0.5, linetype="dashed", color = "black") +
#   labs(title = "", x = "Machine Learning Model Confidence Threshold", y = "Precision", colour = "Metadata Attribute",
#        shape = "Metadata Attribute") +
#   scale_colour_manual(values = c("Race.Precision"="#fe7f0e", "Sex.Precision"="#1f78b4ff", "Tumor.Stage.Precision"="#2ba02dff"), labels = c("Race", "Sex", "Tumor Stage")) +
#   scale_shape_manual(values = c("Race.Precision" = 16, "Sex.Precision" = 17, "Tumor.Stage.Precision" = 15), labels = c("Race", "Sex", "Tumor Stage")) +
#   theme_bw() +
#   theme(axis.text.x = element_text(size = 10),
#         axis.text.y = element_text(size = 10),
#         strip.background = element_rect(colour = "white", fill = "white"),
#         strip.text.x = element_text(size = 15),
#         axis.title.x = element_text(size = 15),
#         axis.title.y = element_text(size = 15),)+
#   scale_x_continuous(breaks = data_long$Threshold) # Ensure breaks are set correctly
# # Display the plot
# ggsave("results/precision_chart.png", width = 12, height = 6, dpi = 300)

###Just make a bar chart...

data_at_05 <- data[data$Threshold == 0.5, ]
data_long <- tidyr::pivot_longer(data_at_05, cols = -Threshold, names_to = "PrecisionType", values_to = "Precision")

ggplot(data_long, aes(x = PrecisionType, y = Precision, fill = PrecisionType)) + 
  geom_bar(stat = "identity") + 
  geom_text(aes(label = paste0(round(Precision, 2))),
          position = position_dodge(width = 0.9),
          vjust = -0.25,
          size = 5,
          color = "black") +
  labs(title = "", 
       x = "", 
       y = "Precision") +
  theme_bw() + 
  theme(axis.text.x = element_text(size = 25),
        axis.text.y = element_text(size = 15),
        strip.background = element_rect(colour = "white", fill = "white"),
        strip.text.x = element_text(size = 25),
        axis.title.x = element_text(size = 25),
        axis.title.y = element_text(size = 25), 
        legend.position = "none") +
  scale_x_discrete(labels = c("Race.Precision" = "Race", 
                              "Sex.Precision" = "Sex", 
                              "Tumor.Stage.Precision" = "Tumor Stage")) + 
  scale_fill_manual(values = c("Sex.Precision" = "#1f77b4", "Race.Precision" = "#ff7f0e", "Tumor.Stage.Precision" = "#44546a")) #
#alternative colors for tumor stage?
ggsave("results/precision_bar_chart.png", width = 12, height = 7, dpi = 300)
