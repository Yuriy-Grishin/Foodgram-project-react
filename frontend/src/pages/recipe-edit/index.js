import { Container, ProductsSearch, FileInput, Input, Title, CheckboxGroup, Main, Form, Button, Checkbox, Textarea } from '../../components'
import styles from './styles.module.css'
import api from '../../api'
import { useEffect, useState } from 'react'
import { useTags } from '../../utils'
import { useParams, useHistory } from 'react-router-dom'
import MetaTags from 'react-meta-tags'

const RecipeEdit = ({ onItemDelete }) => {
  const { value, handleChange, setValue } = useTags()
  const [ recipeName, setRecipeName ] = useState('')

  const [ productValue, setProductValue ] = useState({
    name: '',
    id: null,
    amount: '',
    measurement_unit: ''
  })

  const [ recipeProducts, setRecipeProducts ] = useState([])
  const [ recipeText, setRecipeText ] = useState('')
  const [ recipeTime, setRecipeTime ] = useState(0)
  const [ recipeFile, setRecipeFile ] = useState(null)
  const [
    recipeFileWasManuallyChanged,
    setRecipeFileWasManuallyChanged
  ] = useState(false)

  const [ products, setProducts ] = useState([])
  const [ showProducts, setShowProducts ] = useState(false)
  const [ loading, setLoading ] = useState(true)
  const history = useHistory()

  useEffect(_ => {
    if (productValue.name === '') {
      return setProducts([])
    }
    api
      .getProducts({ name: productValue.name })
      .then(products => {
        setProducts(products)
      })
  }, [productValue.name])

  useEffect(_ => {
    api.getTags()
      .then(tags => {
        setValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getRecipe ({
      recipe_id: id
    }).then(res => {
      const {
        image,
        tags,
        cooking_time,
        name,
        products,
        text
      } = res
      setRecipeText(text)
      setRecipeName(name)
      setRecipeTime(cooking_time)
      setRecipeFile(image)
      setRecipeProducts(products)


      const tagsValueUpdated = value.map(item => {
        item.value = Boolean(tags.find(tag => tag.id === item.id))
        return item
      })
      setValue(tagsValueUpdated)
      setLoading(false)
    })
    .catch(err => {
      history.push('/recipes')
    })
  }, [value])

  const handleProductAutofill = ({ id, name, measurement_unit }) => {
    setProductValue({
      ...productValue,
      id,
      name,
      measurement_unit
    })
  }

  const checkIfDisabled = () => {
    return recipeText === '' ||
    recipeName === '' ||
    recipeProducts.length === 0 ||
    value.filter(item => item.value).length === 0 ||
    recipeTime === '' ||
    recipeFile === '' ||
    recipeFile === null
  }

  return <Main>
    <Container>
      <MetaTags>
        <title>Редактирование рецепта</title>
        <meta name="description" content="Продуктовый помощник - Редактирование рецепта" />
        <meta property="og:title" content="Редактирование рецепта" />
      </MetaTags>
      <Title title='Редактирование рецепта' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          const data = {
            text: recipeText,
            name: recipeName,
            products: recipeProducts.map(item => ({
              id: item.id,
              amount: item.amount
            })),
            tags: value.filter(item => item.value).map(item => item.id),
            cooking_time: recipeTime,
            image: recipeFile,
            recipe_id: id
          }
          api
            .updateRecipe(data, recipeFileWasManuallyChanged)
            .then(res => {
              history.push(`/recipes/${id}`)
            })
            .catch(err => {
              const { non_field_errors, products, cooking_time } = err
              console.log({  products })
              if (non_field_errors) {
                return alert(non_field_errors.join(', '))
              }
              if (products) {
                return alert(`Ингредиенты: ${products.filter(item => Object.keys(item).length).map(item => {
                  const error = item[Object.keys(item)[0]]
                  return error && error.join(' ,')
                })[0]}`)
              }
              if (cooking_time) {
                return alert(`Время готовки: ${cooking_time[0]}`)
              }
              const errors = Object.values(err)
              if (errors) {
                alert(errors.join(', '))
              }
            })
        }}
      >
        <Input
          label='Название рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeName(value)
          }}
          value={recipeName}
        />
        <CheckboxGroup
          label='Теги'
          values={value}
          className={styles.checkboxGroup}
          labelClassName={styles.checkboxGroupLabel}
          tagsClassName={styles.checkboxGroupTags}
          checkboxClassName={styles.checkboxGroupItem}
          handleChange={handleChange}
        />
        <div className={styles.products}>
          <div className={styles.productsInputs}>
            <Input
              label='Ингредиенты'
              className={styles.productsNameInput}
              inputClassName={styles.productsInput}
              labelClassName={styles.productsLabel}
              onChange={e => {
                const value = e.target.value
                setProductValue({
                  ...productValue,
                  name: value
                })
              }}
              onFocus={_ => {
                setShowProducts(true)
              }}
              value={productValue.name}
            />
            <div className={styles.productsAmountInputContainer}>
              <Input
                className={styles.productsAmountInput}
                inputClassName={styles.productsAmountValue}
                onChange={e => {
                  const value = e.target.value
                  setProductValue({
                    ...productValue,
                    amount: value
                  })
                }}
                value={productValue.amount}
              />
              {productValue.measurement_unit !== '' && <div className={styles.measurementUnit}>{productValue.measurement_unit}</div>}
            </div>
            {showProducts && products.length > 0 && <ProductsSearch
              products={products}
              onClick={({ id, name, measurement_unit }) => {
                handleProductAutofill({ id, name, measurement_unit })
                setProducts([])
                setShowProducts(false)
              }}
            />}
          </div>
          <div className={styles.productsAdded}>
            {recipeProducts.map(item => {
              return <div
                className={styles.productsAddedItem}
              >
                <span className={styles.productsAddedItemTitle}>{item.name}</span> <span>-</span> <span>{item.amount}{item.measurement_unit}</span> <span
                  className={styles.productsAddedItemRemove}
                  onClick={_ => {
                    const recipeProductsUpdated = recipeProducts.filter(product => {
                      return product.id !== item.id
                    })
                    setRecipeProducts(recipeProductsUpdated)
                  }}
                >Удалить</span>
              </div>
            })}
          </div>
          <div
            className={styles.productAdd}
            onClick={_ => {
              if (productValue.amount === '' || productValue.name === '') { return }
              setRecipeProducts([...recipeProducts, productValue])
              setProductValue({
                name: '',
                id: null,
                amount: '',
                measurement_unit: ''
              })
            }}
          >
            Добавить ингредиент
          </div>
        </div>
        <div className={styles.cookingTime}>
          <Input
            label='Время приготовления'
            className={styles.productsTimeInput}
            labelClassName={styles.cookingTimeLabel}
            inputClassName={styles.productsTimeValue}
            onChange={e => {
              const value = e.target.value
              setRecipeTime(value)
            }}
            value={recipeTime}
          />
          <div className={styles.cookingTimeUnit}>мин.</div>
        </div>
        <Textarea
          label='Описание рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeText(value)
          }}
          value={recipeText}
        />
        <FileInput
          onChange={file => {
            setRecipeFileWasManuallyChanged(true)
            setRecipeFile(file)
          }}
          className={styles.fileInput}
          label='Загрузить фото'
          file={recipeFile}
        />
        <div className={styles.actions}>
          <Button
            modifier='style_dark-blue'
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Редактировать рецепт
          </Button>
          <div
            className={styles.deleteRecipe}
            onClick={_ => {
              api.deleteRecipe({ recipe_id: id })
                .then(res => {
                  onItemDelete && onItemDelete()
                  history.push('/recipes')
                })
            }}
          >
            Удалить
          </div>
        </div>
      </Form>
    </Container>
  </Main>
}

export default RecipeEdit
