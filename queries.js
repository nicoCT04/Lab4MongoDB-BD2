db.cars.findOne({})

// Agregación para Relación entre volumen de ventas e ingresos por marca

db.cars.aggregate([
  {
    $group: {
      _id: "$brand",
      total_units: { $sum: "$units_sold" },
      total_revenue: { $sum: "$revenue_usd" }
    }
  },
  {
    $project: {
      brand: "$_id",
      total_units: 1,
      total_revenue: 1,
      _id: 0
    }
  }
])