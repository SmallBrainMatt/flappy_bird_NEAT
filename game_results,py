pip install neat-python matplotlib seaborn numpy pandas

import neat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# Example structure:
data = {
    "Generation": [],
    "Best_Fitness": [],
    "Average_Fitness": [],
    "Num_Species": [],
    "Average_Score": [],
    "Max_Score": [],
    "Average_Complexity": [],  # nodes/connections count
}

# (populate this during your NEAT training)

df = pd.read_csv('neat_results.csv')  # Your results file
df.head()

#Plot & Save Fitness Over Generations,Number of Species Over Generations,Genome Complexity Over Generations
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Fitness
sns.lineplot(ax=axes[0, 0], x='Generation', y='Best_Fitness', data=df, color='blue', label='Best Fitness')
axes[0, 0].set_title('Best Fitness')

# Complexity
sns.lineplot(ax=axes[0, 1], x='Generation', y='Average_Complexity', data=df, color='green', label='Complexity')
axes[0, 1].set_title('Genome Complexity')

# Scores
sns.lineplot(ax=axes[1, 0], x='Generation', y='Max_Score', data=df, color='darkblue', label='Max Score')
axes[1, 0].set_title('Max Score Over Generations')

# Species
sns.lineplot(ax=axes[1, 1], x='Generation', y='Num_Species', data=df, color='purple', label='Species Count')
axes[1, 1].set_title('Species Over Generations')

plt.tight_layout()
plt.savefig('combined_metrics.png', dpi=300)
plt.show()



# Plot & Save Scores Over Generations
plt.figure(figsize=(10, 6))
plt.plot(df['Generation'], df['Average_Score'], label='Average Score', color='skyblue', linewidth=2)
plt.plot(df['Generation'], df['Max_Score'], label='Max Score', color='darkblue', linestyle='--')
plt.xlabel('Generation')
plt.ylabel('Score (Pipes Passed)')
plt.title('Score Improvement Over Generations')
plt.legend()
plt.tight_layout()
plt.savefig('scores_over_generations.png', dpi=300)  # Save as PNG
plt.show()


#Smooth fitness trend
df['Rolling_Avg_Fitness'] = df['Average_Fitness'].rolling(window=3, min_periods=1).mean()
plt.figure(figsize=(10, 6))
sns.lineplot(x='Generation', y='Rolling_Avg_Fitness', data=df, color='green', label='Smoothed Avg Fitness')
plt.title('Smoothed Fitness Trend')
plt.grid(True)
plt.savefig('smoothed_fitness.png', dpi=300)
plt.show()

#Fitness over generations
plt.figure(figsize=(10, 6))
sns.lineplot(x='Generation', y='Best_Fitness', data=df, label='Best Fitness', marker='o')
sns.lineplot(x='Generation', y='Avg_Fitness', data=df, label='Average Fitness', marker='s')
plt.title('Fitness Over Generations')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Mean distance Over generations
plt.figure(figsize=(10, 6))
sns.lineplot(x='Generation', y='Mean_Distance', data=df, color='purple', marker='o')
plt.title('Mean Genetic Distance Over Generations')
plt.xlabel('Generation')
plt.ylabel('Mean Distance')
plt.grid(True)
plt.tight_layout()
plt.show()

