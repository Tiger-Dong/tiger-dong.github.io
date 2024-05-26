from django.db import models

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # B/A
    theory_shares_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    chemial_A_mass = models.DecimalField(max_digits=10, decimal_places=2)
    
    chemicalData_B = {
            "b0" : {"nco": 12.8, "functionality": 2, "molecule_quality": 7000 },
    }
    chemical_B_NCO = models.DecimalField(max_digits=10, decimal_places=2, default=chemicalData_B["b0"]["nco"])
    chemical_B_functionality = models.IntegerField(default=chemicalData_B["b0"]["functionality"])
    chemical_B_molecular_mass = models.IntegerField(default=chemicalData_B["b0"]["molecule_quality"])
    chemical_B_mass = models.IntegerField(default=0)
    
    temperature = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    def __str__(self):
        return self.name
    
    
class Chemical_A(models.Model):
    chemicalData_A = {
            "PTMG1000": { "name": "PTMG1000", "functionality": 2, "hydroxyl_value": 112.2, "molecule_quality": 1000 },
            "PTMG2000": { "name": "PTMG2000", "functionality": 2, "hydroxyl_value": 56.1, "molecule_quality": 2000 },
            "330N": { "name": "330N", "functionality": 3, "hydroxyl_value": 35, "molecule_quality": 4800 },
            "BDO": { "name": "BDO", "functionality": 2, "hydroxyl_value": 1247, "molecule_quality": 90 },
            "water": { "name": "水", "functionality": 2, "hydroxyl_value": 6233, "molecule_quality": 18 },
            "silicone_oil": { "name": "硅油", "functionality": 0, "hydroxyl_value": 0, "molecule_quality": 0 },
            "color_paster": { "name": "色膏", "functionality": 0, "hydroxyl_value": 0, "molecule_quality": 0 },
            "catalyst_1": { "name": "催化剂1", "functionality": 0, "hydroxyl_value": 0, "molecule_quality": 0 },
            "catalyst_2": { "name": "催化剂2", "functionality": 0, "hydroxyl_value": 0, "molecule_quality": 0 },
        }
    CHEMICAL_A_CHOICES =[(None, '---------')] + [(key, value["name"]) for key, value in chemicalData_A.items()]
    name = models.CharField(max_length=50, choices=CHEMICAL_A_CHOICES, blank=True)
    functionality = models.IntegerField(default=2)
    hydroxyl = models.DecimalField(max_digits=10, decimal_places=2)
    molecular_mass = models.IntegerField()
    shares = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.job.name}-{self.name}"
    
