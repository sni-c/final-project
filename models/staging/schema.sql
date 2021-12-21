version: 2

models:
  - name: stg_collection
    columns:
      - name: collectionslug
        tests:
          - not_null

  - name: stg_sales
    columns:
      - name: collectionslug
        tests:
          - unique
          - not_null
      - name: nftid
        tests:
          - unique
          - not_null
     