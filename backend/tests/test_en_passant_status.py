import pytest
from engine.Position import Position
from engine.enpassant.EnPassantStatus import EnPassantStatus

def test_initialization():
    status = EnPassantStatus()
    assert not status.available, "Initially, en passant should not be available."
    assert status.eligible_square is None, "No square should be eligible initially."
    assert status.target_pawn_position is None, "There should be no target pawn position initially."
    assert status.pawn_color is None, "There should be no pawn color initially."

def test_set_en_passant_status():
    eligible_square = Position(algebraic="e3")
    target_pawn_position = Position(algebraic="e4")
    status = EnPassantStatus()
    status.set(eligible_square, target_pawn_position, "black")
    
    assert status.available, "En passant should be available after setting."
    assert status.eligible_square == eligible_square, "Eligible square should match the set position."
    assert status.target_pawn_position == target_pawn_position, "Target pawn position should match the set position."
    assert status.pawn_color == "black", "Pawn color should be correctly set."

def test_clear_en_passant_status():
    status = EnPassantStatus()
    status.set(Position(algebraic="e3"), Position(algebraic="e4"), "black")
    status.clear()
    
    assert not status.available, "En passant should not be available after clearing."
    assert status.eligible_square is None, "Eligible square should be None after clearing."
    assert status.target_pawn_position is None, "Target pawn position should be None after clearing."
    assert status.pawn_color is None, "Pawn color should be None after clearing."
