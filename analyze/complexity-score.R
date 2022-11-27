library(spacyr)
library(textplex)
library(tidyverse)
spacy_initialize(model = 'en_core_web_sm')
# df <- read_csv('../factcheckorg.csv', col_names = TRUE)
df_2 <- read_csv('../politifact.csv', col_names = TRUE)

df_2 <- df_2 %>% filter(!is.na(content)) 
content_vector_2 <- df_2$content %>% as.character()
complexity_scores_2 <- calculate_textplex(content_vector_2)
df_2 <- cbind(df_2, complexity_scores_2)
df_2 <- df_2 %>% tibble()
df_2 <- df_2 %>% select(-document)
write_csv(df_2, 'politifact_score.csv', col_names = TRUE)

df <- cbind(df, complexity_scores)
df <- df %>% tibble()
df <- df %>% select(-document)
# write_csv(df, 'factcheckorg_score.csv', col_names = TRUE)

library(furrr)
library(psych)
library(sotu)
library(dplyr)

sotu_text %>% head(5)

data(sotu_rawscore)
fit <- fit_two_factor_model(sotu_rawscore)
sotu_meta$syntactic_complexity <- fit$scores[,1]
sotu_meta$semantic_complexity <- fit$scores[,2]
sotu_meta$text <- sotu_text