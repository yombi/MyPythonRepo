use Data::Dump qw(dump);

foreach ('a'..'z'){
  push(@num_char,$_);
}
for ($i=0;$i<26;$i++){
  $char_num{$num_char[$i]}=$i;
}
sub freq{
  my %freq_table;
  $seq=$_[0];
  $common=$_[1];
  $max=0;
  for ($i=0;$i<length($seq);$i++){
    $char=substr($seq, $i, 1);
    $freq_table{$char}++;
  }
  foreach ('a'..'z'){
    if (exists($freq_table{$_})){
      $freq_table{$_}/=length($seq);
      if($freq_table{$_}>$max){
        $max=$freq_table{$_};
        $char=$_;
      }
    }
  }
  #print $char;
  if($char eq $common){
    return $char;
  }
  $char=$num_char[($char_num{$char}-$char_num{$common})%26];
  return $char;
}
open(FILE,"<",$ARGV[0]) or die $!;
foreach (<FILE>){
  chomp $_;
  $str.=lc $_;
}
$str=~ tr/ //ds;
$str=~ tr/\r//ds;
$str=~ tr/"("//ds;
$str=~ tr/")"//ds;
close (FILE);
for ($p=0;$p<18;$p++){
  $x="";
  for ($z=$p;$z<length($str);$z+=18){
    $x.=substr($str, $z, 1);
  }
  #print"sub: ",$x,"\n";
  #print freq($x),"\n";
  $key.=freq($x,'e');
  #freq($x);
}
print $key;
print"\nEl resultado anterior se obtuvo sabiendo que la e es la letra más comun en
español. ¿Qué posiciones de la llave (empezando en 0) quieres volver a computar y que letra se
asumirá como la más comun?\nSepara todo por comas y al final pon la letra\nok para salir\n";
while($opc=<STDIN>){
  chomp $opc;
  if($opc eq "ok"){
    last;
  }
  @args = split(',', $opc);
  $chr=$args[-1];
  for ($p=0;$p<scalar @args -1;$p++){
    $x="";
    for ($z=$args[$p];$z<length($str);$z+=18){
      $x.=substr($str, $z, 1);
    }
    substr($key,$args[$p],1,freq($x,$chr));
  }
  print "$key\n";
}
