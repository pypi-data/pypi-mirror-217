# Gaussian and Binomial Distributions Python Package

This Python package provides functionality to work with Gaussian and Binomial distributions. It includes classes to represent and perform various operations on these distributions, such as calculating the mean, standard deviation, probability density function (PDF), and more.

## Installation

To install the package, you can use `pip`:
```
pip install dsnd_probabilities_1
```

## Usage

### Gaussian distribution

from dsnd_probabilities_1 import Gaussian

#### Create a Gaussian distribution object
gaussian = Gaussian(0, 1)

#### Calculate the mean of the distribution
mean = gaussian.calculate_mean()

#### Calculate the standard deviation of the distribution
std_dev = gaussian.calculate_stdev()

#### Calculate the probability density function (PDF) for a given value
pdf = gaussian.pdf(0)

#### Add two Gaussian distributions
sum_gaussian = gaussian + Gaussian(2, 3)


### Binomial distribution

from dsnd_probabilities_1 import Binomial

#### Create a Binomial distribution object
binomial = Binomial(0.4, 20)

#### Calculate the mean of the distribution
mean = binomial.calculate_mean()

#### Calculate the standard deviation of the distribution
std_dev = binomial.calculate_stdev()

#### Add two Binomial distributions
sum_binomial = binomial + Binomial(0.6, 20)