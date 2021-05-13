## CS50 AI Week 5 Project: Traffic
### The Experimentation Process
---

**Method:**

I started with some arbitrary values for each of the following variables:
- number of convolutional and pooling layers
- number of filters for convolutional layers
- size of filters for convolutional layers
- pool size for pooling layers
- number of hidden layers
- sizes of hidden layers
- dropout

Then varied the variables one by one.

When the results from a particular value of the variable being tested are better than the results from its other values, this superior value was adopted, and I moved on to vary another variable.

<br>

**Findings:**

*Compiled results from a total of 22 runs.*

1. Number of convolutional and pooling layers
    - With only one pair of convolutional layer and pooling layer, accuracy is high but came at a high loss
    - After adding another pair, accuracy increased slightly with a significant decrease in loss, but a longer time taken
    - Three pairs seemed to be the optimal, with a high accuracy and moderately low loss

2. Number of filters
    - Deviating far from 35 filters, accuracy decreased, loss increased, and time increased
    - However, increasing the filter number slightly seemed to do accuracy an extremely small favour.

3. Filter Size
    - 3x3 looked like the optimal size in this case
    - 4x4 yielded a lower accuracy and higher loss
    - 2x2 resulted in a much lower accuracy and significant loss

4. Pool Size
    - Most likely optimal at 2x2

5. Number of hidden layers
    - As the number increased, accuracy increased, loss decreased, and time decreased
    - This stopped at five hidden layers; with six hidden layers, accuracy fell and loss rose

6. Size of hidden layer
    - Slight deviation from 120 units caused a small decrease in accuracy and increase in loss

7. Dropout
    - At a dropout rate of 0.5, accuracy was hardly past 0.5 and loss was high
    - With a dropout rate of 0.25, accuracy was almost negligible while loss was enormous
    - No dropout worked best

<br>

**Best Results Obtained:**

Time: 5s <br>
Loss: 0.1680 <br>
Accuracy: 0.9554
