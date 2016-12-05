$fn = 83;
$R1 = 0.035;
$R2 = 0.015;

union()
{

translate([0.0, 0.0, -0.11])
{
    cylinder(h=0.11, r1=$R1, r2=$R1,center=false);
}


cylinder(h=0.05, r1=$R1, r2=$R2,center=false);


translate([0.0, 0.0, 0.05])
{
    cylinder(h=0.26, r1=$R2, r2=$R2,center=false);
    }

}