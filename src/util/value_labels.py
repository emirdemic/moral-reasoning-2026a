from types import MappingProxyType

GENDER = MappingProxyType({1: "Female", 2: "Male"})
EDUCATION = MappingProxyType(
    {
        1: "No formal education",
        2: "Primary school",
        3: "High school",
        4: "Undergrad or vocational school",
        5: "Master's degree",
        6: "PhD or higher",
    }
)
HOMETOWN_SIZE = MappingProxyType(
    {
        1: "500k or more",
        2: "200k-499k",
        3: "100-199k",
        4: "99k or less",
    }
)
SES = MappingProxyType(
    {
        1: "Significantly worse",
        2: "Somewhat worse",
        3: "Similar",
        4: "Somewhat better",
        5: "Significantly better",
    }
)
