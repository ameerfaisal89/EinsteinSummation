# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:03:16 2015

@author: Ameer Asif Khan
"""

import numpy as np;

def combo( n ):
    combination = [ 0 ] * len( n );
    
    while ( True ):
        yield tuple( combination );
        
        p = len( n ) - 1;        
        combination[ p ] += 1;
        
        while ( combination[ p ] == n[ p ] ):
            combination[ p ] = 0;
            p -= 1;
            
            if ( p < 0 ):
                return;
            
            combination[ p ] += 1;

#%%
def einSum( subscripts, *operands ):
    subscripts = subscripts.split( "->" );
    lhs = subscripts[ 0 ];
    rhs = subscripts[ 1 ];
    
    lhs = lhs.split( "," );
    
    subList = [ ];
    dimDict = { };
    subDict = { };
    indexTracker = { };
    
    for index, subStr in enumerate( lhs ):
        matrix = operands[ index ];
        
        subs = list( subStr.strip( ) );
        subDict[ id( matrix ) ] = [ ];
        
        for subIndex, sub in enumerate( subs ):
            if sub not in subList:
                subList.append( sub );
            
            dimDict[ sub ] = np.shape( matrix )[ subIndex ];
            subDict[ id( matrix ) ].append( sub );
    
    rhs = rhs.strip( );
    rhsDimList = [ dimDict[ index ] for index in list( rhs ) ];
    result = np.zeros( rhsDimList );
    
    subDict[ id( result ) ] = [ ];
    
    for subIndex, sub in enumerate( list( rhs ) ):
        subDict[ id( result ) ].append( sub );
    
    dimList = tuple( [ dimDict[ sub ] for sub in subList ] );
    
    for sub in subList:
        indexTracker[ sub ] = 0;
    
    for indexTuple in combo( dimList ):
        term = 1;
        
        for index, sub in enumerate( subList ):
            indexTracker[ sub ] = indexTuple[ index ];
        
        for matrix in operands:
            matIndices = tuple( [ indexTracker[ sub ] for sub in subDict[ id( matrix ) ] ] );
            term *= matrix[ matIndices ];
        
        matIndices = tuple( [ indexTracker[ sub ] for sub in subDict[ id( result ) ] ] );
        result[ matIndices ] += term;
    
    return result;

#%%

subscripts = "ij,jk->ik";

a = np.reshape( range( 1, 7 ), ( 2, 3 ) );
b = np.reshape( range( 2, 8 ), ( 3, 2 ) );

result = einSum( subscripts, a, b );

print( result );
print( np.einsum( subscripts, a, b ) );
