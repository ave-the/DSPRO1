namespace DCMR.Models;

public class Ingredient
{
    public string? Name { get; set; }
    public float Serving { get; set; }
    public string Micronutrient { get; set; }
    public float AmountMg { get; set; }
    public float PercentageDV { get; set; }
    public bool IsVegetarian { get; set; }
    public bool IsSelected { get; set; }

    
    public override string ToString()
    {
        return Name + " (that typically contains: " + AmountMg + " mg of iron per " + Serving + " )";
    }
}