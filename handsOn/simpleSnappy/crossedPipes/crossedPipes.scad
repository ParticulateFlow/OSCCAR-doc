$fn = 83;
$R=0.1;

union()
{

cylinder(h=0.6, r1=$R, r2=$R,center=false);


translate([0.0, 0.3, 0.3])
{
    rotate([90, 0, 0])
    {
    cylinder(h=0.6, r1=$R, r2=$R,center=false);
    }
}
}