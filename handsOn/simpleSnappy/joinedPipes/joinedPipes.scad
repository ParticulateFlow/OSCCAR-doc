$fn = 83;

union()
{

cylinder(h=0.4, r1=0.2, r2=0.2,center=false);


translate([0.1, 0.0, 0.2])
{
    rotate([90, 0, 0])
    {
    cylinder(h=0.4, r1=0.05, r2=0.05,center=false);
    }
}
}