import styles from './styles.module.css'

const products = ({ products }) => {
  if (!products) { return null }
  return <div className={styles.products}>
    <h3 className={styles['products__title']}>Ингредиенты:</h3>
    <div className={styles['products__list']}>
      {products.map(({
        name,
        amount,
        measurement_unit
      }) => <p
        key={`${name}${amount}${measurement_unit}`}
        className={styles['products__list-item']}
      >
        {name} - {amount} {measurement_unit}
      </p>)}
    </div>
  </div>
}

export default products

