// Models/Ingredient.cs
namespace DCMR.Shared.Models
{
    public class Ingredient
    {
        public string? Name { get; set; }
        public float Serving { get; set; }
        public float AmountMg { get; set; }
        public float PercentageDV { get; set; }
        public bool IsVegetarian { get; set; }
        public bool IsSelected { get; set; }
    }
}