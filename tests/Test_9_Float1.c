long long main() //long long got incorrectly tokenized
{
    float a = 10, b = 10.0 , c = 10.01 , d = 01.01 ;
    float e = 00.01 , f = 0.0 , g = -0.5 , h = -0.05 ;
    float i = -.5 , j = .50 , k = .05 , l = .050 , m = .0050 ;
    float n = .00501 , o = 010.010 ;
    float p = --0.05 ;

    // invalid floats
    float p = 0..5 , q = 50,05 , r = 50.05.0 , s = 0x.5 ;
    float t = 0.0x5 , u = 0ab ;
    float v = 0x=5 ;

    // valid floats
    float aa = 0x5 ;
    float ab = 0x0.3p10 ;
    return ;
}