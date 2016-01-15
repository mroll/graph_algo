package require math::statistics


# rename map function
interp alias {} map {} ::math::statistics::map

proc n-by-n { n } {
    set matrix {}
    for {set i 0} {$i < $n} {incr i} { lappend matrix {} }
    set matrix
}

proc new-pred-array { oldPI oldD k } {
    set n [llength $oldD]
    set pi [n-by-n $n]

    for {set i 0} {$i < $n} {incr i} {
        for {set j 0} {$j < $n} {incr j} {
            set old_dij [lindex $oldD $i $j]
            set old_dik [lindex $oldD $i $k-1]
            set old_dkj [lindex $oldD $k-1 $j]

            if { $old_dij <= $old_dik + $old_dkj } {
                set pred [lindex $oldPI $i $j]
            } else {
                set pred [lindex $oldPI $k-1 $j]
            }
            lset pi $i $j $pred
        }
    }

    set pi
}

proc init-pred-array { W } {
    set n  [llength $W]
    set pi [n-by-n $n]

    for {set i 0} {$i < $n} {incr i} {
        for {set j 0} {$j < $n} {incr j} {
            if {$i == $j || [lindex $W $i $j] == Inf} {
                lset pi $i $j NIL
            } else {
                lset pi $i $j [expr { $i+1 }]
            }
        }
    }

    set pi
}

proc floyd-warshall { W } {
    set n [llength $W]
    set D0  $W
    set PI0 [init-pred-array $W]
    set step-matrices {}

    lappend step-matrices [list $D0 $PI0]

    for {set k 1} {$k <= $n} {incr k} {
        set D$k [n-by-n $n]
        for {set i 0} {$i < $n} {incr i} {
            for {set j 0} {$j < $n} {incr j} {
                set old_dij [lindex [set D[expr { $k - 1 }]] $i $j]
                set old_dik [lindex [set D[expr { $k - 1 }]] $i $k-1]
                set old_dkj [lindex [set D[expr { $k - 1 }]] $k-1 $j]

                lset D$k $i $j [expr { min($old_dij, $old_dik + $old_dkj) }]
            }
        }
        set PI$k [new-pred-array [set PI[expr { $k - 1 }]] \
                                 [set D[expr { $k - 1 }]] \
                                 $k]

        lappend step-matrices [list [set D$k] [set PI$k]]
    }

    set step-matrices
}

proc max-item-length { lst } {
    set maxlen 0
    foreach item $lst {
        if { [string length $item] > $maxlen } {
            set maxlen [string length $item]
        }
    }

    set maxlen
}

proc row-formatter { m } {
    set spacing [lindex [lsort -real -decreasing [map x $m { [max-item-length $x] }]] 0]
    concat [lrange [string repeat "%-[set spacing]s & " [llength [lindex $m 0]]] 0 end-1] "\\\\"
}

proc pmatrix { m {name {}} } {
    set fmtstr  [row-formatter $m]

    if { [llength $name] > 0 } {
        set pmatrix [list "$name ="]
    } else {
        set pmatrix {}
    }
    lappend pmatrix {\begin{pmatrix}}

    foreach row $m {
        lappend pmatrix [format $fmtstr {*}$row]
    }
    lappend pmatrix {\end{pmatrix}}

    set pmatrix
}

proc boolsearch { lst var script } {
    set indices {}
    for {set i 0} {$i < [llength $lst]} {incr i} {
        if { [apply {*}[subst {{ {$var} {$script} }}] [lindex $lst $i]] } {
            lappend indices $i
        }
    }

    set indices
}

proc boolreplace { lst var script symb } {
    set list $lst
    foreach i [boolsearch $lst $var $script] { lset list $i $symb }
    set list
}

proc lprint { lst } { foreach row $lst { puts $row } }

set W [subst { { 0   Inf Inf Inf -1  Inf }
               { 1   0   Inf 2   Inf Inf }
               { Inf 2   0   Inf Inf -8  }
               { -4  Inf Inf 0   3   Inf }
               { Inf 7   Inf Inf 0   Inf }
               { Inf 5   10  Inf Inf 0   } }]

proc fmt-D-matrix { m k } {
    pmatrix [map row $m { [boolreplace $row el { string equal \$el Inf } {\\infty}] }] [subst { D^{($k)} }]
}

proc fmt-Pi-matrix { m k } {
    pmatrix [map row $m { [boolreplace $row el { string equal \$el NIL } {\\text{NIL}}] }] [subst { \\Pi^{($k)} }]
}

set pairs [floyd-warshall $W]

for {set i 0} {$i < [llength $pairs]} {incr i} {
    puts {\[}
    lprint [fmt-D-matrix  [lindex $pairs $i 0] $i]
    puts "\\, \\\\"
    lprint [fmt-Pi-matrix [lindex $pairs $i 1] $i]
    puts {\]}
    puts "\n\n"
}
