# Fuzzy Search User Matching System

A Python-based fuzzy search system for finding users based on their username, first name, and last name using Burkhard-Keller Tree (BK-Tree) data structure and Levenshtein distance algorithm.

## Overview

This system provides intelligent user search capabilities with support for typos, partial matches, and weighted scoring across multiple user attributes. It returns a ranked list of usernames based on relevance, with configurable weighting schemes for multi-word queries.

## Features

- **Multi-field Search**: Search across username, firstname, and lastname simultaneously
- **Fuzzy Matching**: Handles typos and approximate matches using Levenshtein distance
- **Weighted Scoring**: Configurable weights for different fields (username: 50%, firstname: 30%, lastname: 20%)
- **Smart Ranking**: Advanced scoring with prefix matching, substring matching bonuses
- **Multi-word Support**: Handle sentence-based queries with exponential or linear word position weighting
- **Adaptive Distance**: Automatically adjusts search distance based on query length
- **Threshold Filtering**: Filter results based on minimum relevance score

## Installation

### Dependencies

```bash
pip install pybktree numpy
```

### Required Files

- `example.py` - Main fuzzy search implementation
- User data in JSON format with username, firstname, lastname fields

## Usage

### Basic Setup

```python
from NearMatch import FuzzySearch
from  data_gen import  generate_mock_users

mock_data = generate_mock_users(10)

search = FuzzySearch(mock_data)
search.build_tree()


```

### Single Word Search

```python
# Search for single word - returns ranked usernames
results = fuzzy_search.sentence_ranking("john", weightage='exp')
print(results)  # ['john_doe', 'jane_smith', ...]
```

### Multi-word Search with Different Weighting

```python
# Exponential weighting (first word weighted more heavily)
results_exp = fuzzy_search.sentence_ranking("john smith", weightage='exp')

# Linear weighting (more balanced word importance)
results_linear = fuzzy_search.sentence_ranking("john smith", weightage='linear')
```

## Code Logic Explanation

### Core Components

#### 1. **UserData Class**
Simple data container holding user information (username, firstname, lastname).

#### 2. **Levenshtein Distance Algorithm**
- Implements dynamic programming approach to calculate edit distance between strings
- Uses space-optimized version with two arrays instead of full matrix
- Measures minimum operations (insert, delete, substitute) to transform one string to another

#### 3. **BK-Tree Data Structure**
- Metric tree that organizes data based on distance metrics
- Enables efficient fuzzy search by pruning search space
- Separate trees built for username, firstname, and lastname fields

#### 4. **Scoring System**
The scoring algorithm considers multiple factors:
- **Base Score**: `1 - (distance / max_length)` - Higher score for closer matches
- **Prefix Bonus**: +0.3 for exact prefix match, +0.1 for same first character
- **Contains Bonus**: +0.15 if search term is substring of found term

#### 5. **Weighted Field Scoring**
- Username: 50% weight (most important)
- Firstname: 30% weight
- Lastname: 20% weight
- Combines scores across all fields for comprehensive matching

#### 6. **Multi-word Position Weighting**
When searching sentences, word position affects relevance:

**Exponential Weighting** (`exp`):
- First word: Full weight (e^0 = 1.0)
- Second word: ~37% weight (e^-1 ≈ 0.37)
- Third word: ~14% weight (e^-2 ≈ 0.14)
- Best for queries where first word is most important

**Linear Weighting** (`linear`):
- First word: Full weight (1/1 = 1.0)
- Second word: 50% weight (1/2 = 0.5)
- Third word: 33% weight (1/3 ≈ 0.33)
- More balanced approach for equal word importance

#### 7. **Adaptive Distance Calculation**
Automatically adjusts search tolerance based on query length:
- Very short queries (≤2 chars): Distance = max(5, length + 3)
- Short queries (3-4 chars): Distance = length + 2
- Longer queries (≥5 chars): Distance = max(2, length ÷ 2)

## Configuration Options

### Threshold Adjustment
```python
# Only return results with score above 0.3 (30% relevance)
fuzzy_search = FuzzySearch(user_data, threshold=0.3)
```

### Custom Field Weights
```python
# Modify after initialization
fuzzy_search.weights = np.array([0.6, 0.25, 0.15])  # More emphasis on username
```

## Return Format

The `sentence_ranking()` method returns a list of usernames sorted by relevance score (highest first). Only usernames exceeding the threshold score are included.

Example output:
```python
['john_doe', 'johnny_appleseed', 'jane_johnson']
```

## Performance Considerations

- **Tree Building**: O(n log n) - Done once during initialization
- **Single Search**: O(log n) average case due to BK-Tree pruning
- **Multi-word Search**: Linear with number of words
- **Memory**: Stores three separate BK-Trees plus original data

## Error Handling

- Raises `ValueError` if trees not built before searching
- Validates weightage type parameters
- Handles empty strings and edge cases in distance calculation

## Use Cases

- User account search with typo tolerance
- Name-based user discovery
- Autocomplete functionality
- Customer support user lookup
- Social platform user finding