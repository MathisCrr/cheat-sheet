[Official YAML Specifications](https://yaml.org/spec/1.2.2/)

```yaml
object:

  # literal string
  key: a string
  key: "a string"
  key: 'a string'

  # literal number
  key: 2 # int
  key: 2.5 # float
  key: 1e+10 # exponential form

  # literal boolean
  key: true

  # literal dates (ISO 8601)
  key: 2001-01-23 10:00:00

  # literal null
  key: null

  # type casting
  key: !!float 10 # 10.0
  gpa: !!str 3.5 # "3.5"



  # list of items
  key: 
    - element 1
    - element 2
  key: ['element 1', "element 2"]

  # list of objects
  key:
  - a: 1
    b: 2
  - {a: 1, b: 2}
  -
    a: 1
    b: 2



  # newline will be removed
  key: >
    Lorem ipsum
    dolor sit
    amet
  
  # formating will be preserved
  key: |
    Lorem ipsum
    dolor sit
    amet



  # anchors literal
  key: &anchor-name "word"
  key: *anchor-name # value will refer to anchor &{ANCHOR}, giving "word" here


  # anchoring object
  base: &anchor-name-obj
    key: 'work'
  foo:  # value will expand to anchor &{ANCHOR}
    <<: *anchor-name-obj
    key2: 'word2'
  # giving:
  # foo:
  #   key: 'work'
  #   key2: 'word2'
```